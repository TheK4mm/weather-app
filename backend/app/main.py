"""Punto de entrada de la API (FastAPI).

Crea la aplicación, configura CORS, registra los routers y los manejadores
de excepciones.

Ejecutar en desarrollo:
    uvicorn app.main:app --reload
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, weather
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API que consume OpenWeatherMap y expone clima actual y pronóstico.",
)

# CORS: permite que el frontend (Vue / Vite) consuma esta API desde el navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejadores que convierten las excepciones de dominio en JSON consistente.
register_exception_handlers(app)

# Routers bajo el prefijo común /api.
app.include_router(health.router, prefix="/api")
app.include_router(weather.router, prefix="/api")


@app.get("/", tags=["root"], summary="Información de la API")
async def root() -> dict:
    """Endpoint raíz con metadatos básicos."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
    }
