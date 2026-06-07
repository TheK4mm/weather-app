"""Cliente de integración con OpenWeatherMap.

Es la ÚNICA capa que conoce los detalles del proveedor externo: URLs,
parámetros y autenticación. Devuelve el JSON crudo (``dict``) y traduce
los errores HTTP del proveedor a excepciones de dominio.

Gracias a esta separación, cambiar de proveedor (p. ej. a WeatherAPI.com)
solo implica crear otro cliente con los mismos métodos: el servicio y el
resto de capas no se modifican.
"""
from __future__ import annotations

import httpx

from app.core.config import Settings
from app.core.exceptions import CityNotFoundError, MissingApiKeyError, UpstreamError


class OpenWeatherClient:
    """Wrapper asíncrono sobre la API de OpenWeatherMap (endpoints 2.5 gratuitos)."""

    CURRENT_PATH = "/data/2.5/weather"
    FORECAST_PATH = "/data/2.5/forecast"

    def __init__(self, settings: Settings) -> None:
        self._api_key = settings.owm_api_key
        self._base_url = settings.owm_base_url.rstrip("/")
        self._timeout = settings.owm_timeout

    async def get_current(self, city: str, units: str, lang: str) -> dict:
        """Devuelve el clima actual crudo de una ciudad."""
        return await self._get(self.CURRENT_PATH, {"q": city, "units": units, "lang": lang})

    async def get_forecast(self, city: str, units: str, lang: str) -> dict:
        """Devuelve el pronóstico crudo (5 días / cada 3 h) de una ciudad."""
        return await self._get(self.FORECAST_PATH, {"q": city, "units": units, "lang": lang})

    async def _get(self, path: str, params: dict) -> dict:
        """Ejecuta el GET, adjunta la API key y traduce los errores HTTP."""
        if not self._api_key:
            raise MissingApiKeyError()

        url = f"{self._base_url}{path}"
        query = {**params, "appid": self._api_key}

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.get(url, params=query)
        except httpx.RequestError as exc:
            # Falla de red, DNS o timeout: no llegamos al proveedor.
            raise UpstreamError(
                "No se pudo conectar con el proveedor de datos meteorológicos."
            ) from exc

        # Traducción de códigos de error del proveedor a excepciones de dominio.
        if response.status_code == httpx.codes.NOT_FOUND:
            raise CityNotFoundError()
        if response.status_code == httpx.codes.UNAUTHORIZED:
            raise MissingApiKeyError("La API key de OpenWeatherMap no es válida.")
        if response.status_code >= 400:
            raise UpstreamError()

        return response.json()
