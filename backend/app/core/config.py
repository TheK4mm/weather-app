"""Configuración central de la aplicación.

Carga los ajustes desde variables de entorno / archivo ``.env`` usando
``pydantic-settings``. De esta forma NINGÚN secreto (como la API key de
OpenWeatherMap) queda escrito en el código fuente.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Ajustes de la aplicación leídos del entorno (.env)."""

    # --- OpenWeatherMap ---
    owm_api_key: str = ""                                  # API key (obligatoria en runtime real)
    owm_base_url: str = "https://api.openweathermap.org"   # URL base del proveedor
    owm_timeout: float = 10.0                              # timeout (segundos) de las peticiones HTTP

    # --- Valores por defecto del dominio ---
    default_units: str = "metric"                          # metric (°C) | imperial (°F)
    default_lang: str = "es"                               # idioma de las descripciones

    # --- Caché ---
    cache_ttl: int = 600                                   # segundos que se reutiliza una respuesta (10 min)
    cache_maxsize: int = 256                               # nº máximo de entradas en caché

    # --- CORS ---
    # Orígenes del frontend permitidos, separados por comas.
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # --- Metadatos de la API ---
    app_name: str = "Weather API"
    app_version: str = "1.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Convierte la cadena de orígenes CORS en una lista limpia."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Devuelve una instancia única (cacheada) de ``Settings``.

    Se usa como dependencia de FastAPI para inyectar la configuración.
    """
    return Settings()


# Instancia global de conveniencia.
settings = get_settings()
