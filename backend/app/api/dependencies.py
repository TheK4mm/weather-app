"""Dependencias de FastAPI: construcción e inyección de las capas.

Centraliza el "cableado" (wiring):
    configuración -> cliente -> servicio -> controlador
de modo que las rutas solo pidan el controlador ya listo.

El uso de ``lru_cache`` convierte al controlador (y por tanto a la caché
del servicio) en un singleton que persiste entre peticiones.
"""
from __future__ import annotations

from functools import lru_cache

from app.api.controllers.weather_controller import WeatherController
from app.core.config import get_settings
from app.integrations.openweather_client import OpenWeatherClient
from app.services.weather_service import WeatherService


@lru_cache
def _build_controller() -> WeatherController:
    settings = get_settings()
    client = OpenWeatherClient(settings)
    service = WeatherService(client, settings)
    return WeatherController(service)


def get_weather_controller() -> WeatherController:
    """Provee el controlador del clima (con su servicio y caché)."""
    return _build_controller()
