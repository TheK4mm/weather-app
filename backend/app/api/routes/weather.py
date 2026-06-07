"""Rutas HTTP del clima.

Declaran los endpoints, validan los parámetros de entrada (longitud,
rangos, valores permitidos) y delegan en el controlador. No contienen
lógica de negocio.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.api.controllers.weather_controller import WeatherController
from app.api.dependencies import get_weather_controller
from app.core.exceptions import WeatherAPIError
from app.schemas.weather import (
    CurrentWeather,
    ErrorResponse,
    ForecastDay,
    Units,
    WeatherBundle,
)

router = APIRouter(prefix="/weather", tags=["weather"])

# Respuestas de error documentadas en /docs.
ERROR_RESPONSES = {
    404: {"model": ErrorResponse, "description": "Ciudad no encontrada"},
    502: {"model": ErrorResponse, "description": "Error del proveedor externo"},
    503: {"model": ErrorResponse, "description": "API key no configurada"},
}


@router.get(
    "",
    response_model=WeatherBundle,
    responses=ERROR_RESPONSES,
    summary="Clima actual + pronóstico",
)
async def get_weather(
    city: str = Query(..., min_length=1, max_length=100, description="Nombre de la ciudad"),
    units: Units = Query(Units.metric, description="Sistema de unidades"),
    lang: str = Query("es", min_length=2, max_length=5, description="Idioma de las descripciones"),
    days: int = Query(5, ge=1, le=5, description="Número de días de pronóstico"),
    controller: WeatherController = Depends(get_weather_controller),
) -> WeatherBundle:
    """Devuelve el clima actual y el pronóstico de varios días de una ciudad."""
    return await controller.get_weather_bundle(city, units.value, lang, days)


@router.get(
    "/current",
    response_model=CurrentWeather,
    responses=ERROR_RESPONSES,
    summary="Solo clima actual",
)
async def get_current(
    city: str = Query(..., min_length=1, max_length=100, description="Nombre de la ciudad"),
    units: Units = Query(Units.metric, description="Sistema de unidades"),
    lang: str = Query("es", min_length=2, max_length=5, description="Idioma de las descripciones"),
    controller: WeatherController = Depends(get_weather_controller),
) -> CurrentWeather:
    """Devuelve únicamente el clima actual de una ciudad."""
    return await controller.get_current(city, units.value, lang)


@router.get(
    "/forecast",
    response_model=list[ForecastDay],
    responses=ERROR_RESPONSES,
    summary="Solo pronóstico",
)
async def get_forecast(
    city: str = Query(..., min_length=1, max_length=100, description="Nombre de la ciudad"),
    units: Units = Query(Units.metric, description="Sistema de unidades"),
    lang: str = Query("es", min_length=2, max_length=5, description="Idioma de las descripciones"),
    days: int = Query(5, ge=1, le=5, description="Número de días de pronóstico"),
    controller: WeatherController = Depends(get_weather_controller),
) -> list[ForecastDay]:
    """Devuelve únicamente el pronóstico de varios días de una ciudad."""
    return await controller.get_forecast(city, units.value, lang, days)
