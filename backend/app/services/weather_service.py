"""Servicio de clima: lógica de negocio.

Orquesta el cliente de integración, transforma la respuesta cruda del
proveedor en nuestros DTOs y agrega el pronóstico de 3 h en resúmenes
diarios. Es agnóstico del proveedor: solo depende de un cliente que
exponga ``get_current`` y ``get_forecast``.

Incluye una caché TTL en memoria para reducir llamadas al proveedor
(menor latencia y respeto de los límites del plan gratuito).
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone

from cachetools import TTLCache

from app.core.config import Settings
from app.integrations.openweather_client import OpenWeatherClient
from app.schemas.weather import CurrentWeather, ForecastDay, Units, WeatherBundle

# Plantilla de URL para los iconos oficiales de OpenWeatherMap.
ICON_URL = "https://openweathermap.org/img/wn/{icon}@2x.png"
DEFAULT_ICON = "01d"


class WeatherService:
    """Lógica de negocio para consultar y normalizar datos del clima."""

    def __init__(self, client: OpenWeatherClient, settings: Settings) -> None:
        self._client = client
        self._settings = settings
        # Caché compartida por instancia del servicio (singleton vía DI).
        self._cache: TTLCache = TTLCache(
            maxsize=settings.cache_maxsize, ttl=settings.cache_ttl
        )

    async def get_weather(
        self, city: str, units: str, lang: str, days: int = 5
    ) -> WeatherBundle:
        """Devuelve clima actual + pronóstico agregado por día."""
        cache_key = f"{city.strip().lower()}|{units}|{lang}|{days}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        raw_current = await self._client.get_current(city, units, lang)
        raw_forecast = await self._client.get_forecast(city, units, lang)

        bundle = WeatherBundle(
            units=Units(units),
            current=self._map_current(raw_current),
            forecast=self._aggregate_forecast(raw_forecast, days),
        )
        self._cache[cache_key] = bundle
        return bundle

    # ------------------------------------------------------------------ #
    # Transformaciones (respuesta cruda del proveedor -> DTOs propios)    #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _map_current(raw: dict) -> CurrentWeather:
        """Mapea el JSON de /weather a nuestro DTO ``CurrentWeather``."""
        weather = (raw.get("weather") or [{}])[0]
        main = raw.get("main", {})
        return CurrentWeather(
            city=raw.get("name", ""),
            country=raw.get("sys", {}).get("country", ""),
            temperature=round(main.get("temp", 0.0), 1),
            feels_like=round(main.get("feels_like", 0.0), 1),
            description=weather.get("description", "").capitalize(),
            icon=ICON_URL.format(icon=weather.get("icon", DEFAULT_ICON)),
            humidity=main.get("humidity", 0),
            wind_speed=raw.get("wind", {}).get("speed", 0.0),
        )

    @classmethod
    def _aggregate_forecast(cls, raw: dict, days: int) -> list[ForecastDay]:
        """Agrupa las entradas de 3 h por día (hora local) y resume cada día.

        OpenWeatherMap entrega ~40 entradas de 3 h. Aquí se agrupan por fecha
        local de la ciudad y se calcula min/máx, además de elegir el icono y
        la descripción de la franja más cercana al mediodía como representativos.
        """
        # Offset horario de la ciudad (en segundos) para trabajar en hora local.
        tz_offset = raw.get("city", {}).get("timezone", 0)
        tzinfo = timezone(timedelta(seconds=tz_offset))

        by_day: dict = defaultdict(list)
        for entry in raw.get("list", []):
            local_dt = datetime.fromtimestamp(entry["dt"], tz=tzinfo)
            by_day[local_dt.date()].append((local_dt, entry))

        result: list[ForecastDay] = []
        for day in sorted(by_day)[:days]:
            entries = by_day[day]
            temps = [entry["main"]["temp"] for _, entry in entries]

            # Franja más cercana al mediodía -> icono/descripción representativos.
            _, noon_entry = min(entries, key=lambda pair: abs(pair[0].hour - 12))
            weather = (noon_entry.get("weather") or [{}])[0]

            result.append(
                ForecastDay(
                    date=day,
                    temp_min=round(min(temps), 1),
                    temp_max=round(max(temps), 1),
                    description=weather.get("description", "").capitalize(),
                    icon=ICON_URL.format(icon=weather.get("icon", DEFAULT_ICON)),
                )
            )
        return result
