"""Fixtures compartidas por las pruebas."""
from __future__ import annotations

import pytest

from app.core.config import Settings
from app.integrations.openweather_client import OpenWeatherClient
from app.services.weather_service import WeatherService


@pytest.fixture
def settings() -> Settings:
    """Settings de prueba con una API key ficticia."""
    return Settings(owm_api_key="test-key", cache_ttl=1)


@pytest.fixture
def service(settings: Settings) -> WeatherService:
    """Servicio del clima con un cliente real (cuyo HTTP se mockea con respx)."""
    client = OpenWeatherClient(settings)
    return WeatherService(client, settings)
