"""Endpoint de salud (health check)."""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Estado del servicio")
async def health() -> dict:
    """Comprueba que la API está viva."""
    return {"status": "ok"}
