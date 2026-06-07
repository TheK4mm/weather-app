"""Controlador del clima.

Capa de orquestación entre las rutas (transporte HTTP) y el servicio
(lógica de negocio). Mantiene las rutas delgadas y centraliza el armado
de la respuesta de cada caso de uso. Reutiliza ``get_weather`` (cacheado)
para los endpoints parciales, evitando llamadas duplicadas al proveedor.
"""
from __future__ import annotations

from app.schemas.weather import CurrentWeather, ForecastDay, WeatherBundle
from app.services.weather_service import WeatherService


class WeatherController:
    """Coordina los casos de uso del clima delegando en el servicio."""

    def __init__(self, service: WeatherService) -> None:
        self._service = service

    async def get_weather_bundle(
        self, city: str, units: str, lang: str, days: int
    ) -> WeatherBundle:
        """Caso de uso principal: clima actual + pronóstico."""
        return await self._service.get_weather(city, units, lang, days)

    async def get_current(self, city: str, units: str, lang: str) -> CurrentWeather:
        """Solo el clima actual."""
        bundle = await self._service.get_weather(city, units, lang)
        return bundle.current

    async def get_forecast(
        self, city: str, units: str, lang: str, days: int
    ) -> list[ForecastDay]:
        """Solo el pronóstico de varios días."""
        bundle = await self._service.get_weather(city, units, lang, days)
        return bundle.forecast
