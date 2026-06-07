"""Pruebas de las rutas HTTP.

Se sustituye el controlador real por un stub mediante
``app.dependency_overrides``, de modo que las pruebas se centren en el
transporte (validación, códigos de estado, forma del JSON) sin tocar la red.
"""
from __future__ import annotations

from datetime import date

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_weather_controller
from app.core.exceptions import CityNotFoundError
from app.main import app
from app.schemas.weather import CurrentWeather, ForecastDay, Units, WeatherBundle

_CURRENT = CurrentWeather(
    city="Bogotá",
    country="CO",
    temperature=18.0,
    feels_like=17.5,
    description="Cielo claro",
    icon="https://openweathermap.org/img/wn/01d@2x.png",
    humidity=70,
    wind_speed=3.2,
)
_FORECAST = [
    ForecastDay(
        date=date(2026, 6, 6),
        temp_min=14.0,
        temp_max=22.0,
        description="Nubes dispersas",
        icon="https://openweathermap.org/img/wn/03d@2x.png",
    )
]


class FakeController:
    """Controlador de prueba que no llama a ningún servicio externo."""

    async def get_weather_bundle(self, city, units, lang, days):
        if city.strip().lower() == "nowhere":
            raise CityNotFoundError()
        return WeatherBundle(units=Units(units), current=_CURRENT, forecast=_FORECAST)

    async def get_current(self, city, units, lang):
        return _CURRENT

    async def get_forecast(self, city, units, lang, days):
        return _FORECAST


@pytest.fixture
def client():
    app.dependency_overrides[get_weather_controller] = lambda: FakeController()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_weather_ok(client):
    response = client.get("/api/weather", params={"city": "Bogota"})
    assert response.status_code == 200
    body = response.json()
    assert body["current"]["city"] == "Bogotá"
    assert body["units"] == "metric"
    assert len(body["forecast"]) == 1


def test_get_weather_city_not_found(client):
    response = client.get("/api/weather", params={"city": "nowhere"})
    assert response.status_code == 404
    assert response.json()["code"] == "city_not_found"


def test_get_weather_requires_city(client):
    """Sin el parámetro obligatorio 'city' -> 422 (validación)."""
    response = client.get("/api/weather")
    assert response.status_code == 422


def test_get_weather_rejects_invalid_units(client):
    response = client.get("/api/weather", params={"city": "Bogota", "units": "kelvin"})
    assert response.status_code == 422
