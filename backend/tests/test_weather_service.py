"""Pruebas de la lógica de negocio (WeatherService).

Se mockea la capa HTTP con ``respx`` para no llamar al proveedor real.
"""
from __future__ import annotations

import respx
from httpx import Response

# --- JSON crudo mínimo, con la forma que devuelve OpenWeatherMap ---

CURRENT_JSON = {
    "name": "Bogotá",
    "sys": {"country": "CO"},
    "main": {"temp": 18.04, "feels_like": 17.52, "humidity": 70},
    "wind": {"speed": 3.2},
    "weather": [{"description": "cielo claro", "icon": "01d"}],
}

FORECAST_JSON = {
    "city": {"timezone": -18000},  # Bogotá (UTC-5)
    "list": [
        {"dt": 1717689600, "main": {"temp": 14.0}, "weather": [{"description": "lluvia ligera", "icon": "10d"}]},
        {"dt": 1717700400, "main": {"temp": 21.0}, "weather": [{"description": "nubes dispersas", "icon": "03d"}]},
        {"dt": 1717776000, "main": {"temp": 13.0}, "weather": [{"description": "cielo claro", "icon": "01d"}]},
        {"dt": 1717786800, "main": {"temp": 22.0}, "weather": [{"description": "muy nuboso", "icon": "04d"}]},
    ],
}


def _mock_owm() -> None:
    """Configura las respuestas mock de los dos endpoints de OpenWeatherMap."""
    respx.get(url__startswith="https://api.openweathermap.org/data/2.5/weather").mock(
        return_value=Response(200, json=CURRENT_JSON)
    )
    respx.get(url__startswith="https://api.openweathermap.org/data/2.5/forecast").mock(
        return_value=Response(200, json=FORECAST_JSON)
    )


@respx.mock
async def test_get_weather_maps_current(service):
    _mock_owm()
    bundle = await service.get_weather("Bogota", "metric", "es")

    assert bundle.units.value == "metric"
    assert bundle.current.city == "Bogotá"
    assert bundle.current.country == "CO"
    assert bundle.current.temperature == 18.0          # redondeado a 1 decimal
    assert bundle.current.feels_like == 17.5
    assert bundle.current.humidity == 70
    assert bundle.current.description == "Cielo claro"  # capitalizado
    assert bundle.current.icon.endswith("/01d@2x.png")


@respx.mock
async def test_get_weather_aggregates_forecast(service):
    _mock_owm()
    bundle = await service.get_weather("Bogota", "metric", "es")

    assert len(bundle.forecast) >= 1
    for day in bundle.forecast:
        assert day.temp_min <= day.temp_max
        assert day.icon.startswith("https://openweathermap.org/img/wn/")
        assert day.description  # no vacío


@respx.mock
async def test_get_weather_uses_cache(service):
    """La segunda llamada idéntica debe servirse de la caché (sin nuevo HTTP)."""
    current_route = respx.get(
        url__startswith="https://api.openweathermap.org/data/2.5/weather"
    ).mock(return_value=Response(200, json=CURRENT_JSON))
    respx.get(url__startswith="https://api.openweathermap.org/data/2.5/forecast").mock(
        return_value=Response(200, json=FORECAST_JSON)
    )

    await service.get_weather("Bogota", "metric", "es")
    await service.get_weather("Bogota", "metric", "es")

    # Solo una llamada real al endpoint de clima actual (la 2ª vino de caché).
    assert current_route.call_count == 1
