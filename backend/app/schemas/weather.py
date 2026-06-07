"""DTOs (Data Transfer Objects) del dominio del clima.

Definen el CONTRATO público de la API: lo que el backend devuelve al
frontend, independiente del formato de OpenWeatherMap. Pydantic se
encarga de la validación y la serialización automática (y de la
documentación en /docs).
"""
from __future__ import annotations

from datetime import date as date_type
from enum import Enum

from pydantic import BaseModel, Field


class Units(str, Enum):
    """Sistemas de unidades soportados."""

    metric = "metric"      # °C, m/s
    imperial = "imperial"  # °F, mph


class CurrentWeather(BaseModel):
    """Clima actual normalizado para una ubicación."""

    city: str = Field(..., description="Nombre de la ciudad")
    country: str = Field(..., description="Código de país (ISO 3166)")
    temperature: float = Field(..., description="Temperatura actual")
    feels_like: float = Field(..., description="Sensación térmica")
    description: str = Field(..., description="Descripción del estado del cielo")
    icon: str = Field(..., description="URL del icono del clima")
    humidity: int = Field(..., description="Humedad relativa (%)")
    wind_speed: float = Field(..., description="Velocidad del viento")


class ForecastDay(BaseModel):
    """Resumen del pronóstico para un día."""

    date: date_type = Field(..., description="Fecha del pronóstico")
    temp_min: float = Field(..., description="Temperatura mínima del día")
    temp_max: float = Field(..., description="Temperatura máxima del día")
    description: str = Field(..., description="Descripción representativa del día")
    icon: str = Field(..., description="URL del icono representativo del día")


class WeatherBundle(BaseModel):
    """Respuesta combinada: clima actual + pronóstico de varios días."""

    units: Units = Field(..., description="Sistema de unidades usado")
    current: CurrentWeather
    forecast: list[ForecastDay]


class ErrorResponse(BaseModel):
    """Formato estándar de error de la API."""

    detail: str = Field(..., description="Mensaje legible del error")
    code: str = Field(..., description="Código corto e identificable del error")
