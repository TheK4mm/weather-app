# Weather API — Backend (FastAPI)

API REST que consume **OpenWeatherMap** y expone un contrato propio y limpio para el
frontend (clima actual + pronóstico de 5 días). La API key vive solo en el servidor.

## Arquitectura por capas

```
routes  ->  controllers  ->  services  ->  integrations (OpenWeatherMap)
(HTTP)      (orquestación)   (negocio)      (consumo del proveedor)
```

- **routes/** — declaran endpoints y validan parámetros.
- **controllers/** — orquestan los casos de uso.
- **services/** — lógica de negocio: normalización, agregación del pronóstico, caché.
- **integrations/** — único módulo que conoce OpenWeatherMap (intercambiable).
- **schemas/** — DTOs Pydantic (contrato público).
- **core/** — configuración (`config.py`) y errores (`exceptions.py`).

## Requisitos

- Python 3.11+
- Una API key gratuita de OpenWeatherMap: https://openweathermap.org/api

## Instalación

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements-dev.txt # incluye runtime + pruebas
```

## Configuración

```powershell
Copy-Item .env.example .env
# Edita .env y coloca tu OWM_API_KEY
```

## Ejecutar

```powershell
uvicorn app.main:app --reload
```

- API:  http://127.0.0.1:8000
- Docs (Swagger UI): http://127.0.0.1:8000/docs

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/health` | Estado del servicio |
| GET | `/api/weather?city=Bogota` | Clima actual + pronóstico (principal) |
| GET | `/api/weather/current?city=Bogota` | Solo clima actual |
| GET | `/api/weather/forecast?city=Bogota&days=5` | Solo pronóstico |

Parámetros comunes: `city` (obligatorio), `units` (`metric`\|`imperial`), `lang` (def. `es`).

## Pruebas

```powershell
pytest
```

Las pruebas mockean el HTTP con `respx` y el controlador con `dependency_overrides`,
por lo que **no consumen** la API real ni requieren API key.
