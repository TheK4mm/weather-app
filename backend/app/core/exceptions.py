"""Excepciones de dominio y sus manejadores HTTP.

Permiten que las capas internas (servicio / cliente) lancen errores
semánticos sin conocer detalles de HTTP, y que FastAPI los traduzca a
respuestas JSON limpias y consistentes (campo ``detail`` + ``code``).
"""
from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class WeatherAPIError(Exception):
    """Error base del dominio del clima."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: str = "weather_error"
    message: str = "Error inesperado al procesar la solicitud del clima."

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message
        super().__init__(self.message)


class CityNotFoundError(WeatherAPIError):
    """La ciudad solicitada no existe en el proveedor."""

    status_code = status.HTTP_404_NOT_FOUND
    code = "city_not_found"
    message = "No se encontró la ciudad solicitada."


class MissingApiKeyError(WeatherAPIError):
    """El servidor no tiene una API key válida configurada."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = "missing_api_key"
    message = "El servidor no tiene configurada una API key válida de OpenWeatherMap."


class UpstreamError(WeatherAPIError):
    """Fallo al comunicarse con el proveedor externo."""

    status_code = status.HTTP_502_BAD_GATEWAY
    code = "upstream_error"
    message = "Error al comunicarse con el proveedor de datos meteorológicos."


def register_exception_handlers(app: FastAPI) -> None:
    """Registra el manejador que convierte ``WeatherAPIError`` en JSON."""

    @app.exception_handler(WeatherAPIError)
    async def _handle_weather_error(_: Request, exc: WeatherAPIError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message, "code": exc.code},
        )
