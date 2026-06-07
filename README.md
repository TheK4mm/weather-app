# Weather App — Full-Stack (FastAPI + Vue 3)

Aplicación del clima reescrita con una arquitectura **full-stack profesional**: un
**backend FastAPI** que consume **OpenWeatherMap** y expone una API limpia, y un
**frontend SPA en Vue 3** que la consume. Permite consultar el **clima actual** y el
**pronóstico de 5 días** de cualquier ciudad.

> Versión anterior: una página estática que llamaba a la API meteorológica directamente
> desde el navegador con la API key expuesta. Esta versión separa responsabilidades por
> capas, oculta la key en el servidor y añade pronóstico.

---

## Arquitectura

Patrón **BFF (Backend-for-Frontend)**: el frontend solo habla con nuestro backend, nunca
con OpenWeatherMap directamente. Así la API key permanece secreta y la lógica se centraliza.

```
┌────────────┐        HTTP/JSON        ┌──────────────────────────────────────────┐
│  Vue 3 SPA │  ───────────────────►   │                 FastAPI                  │
│ (frontend) │  ◄───────────────────   │                                          │
└────────────┘   contrato propio       │  routes → controllers → services →       │
                                       │                          integrations ──┼──► OpenWeatherMap
                                       └──────────────────────────────────────────┘
```

**Backend en capas** (una petición fluye de arriba a abajo):

| Capa | Responsabilidad |
|------|-----------------|
| `routes` | Declarar endpoints y validar parámetros |
| `controllers` | Orquestar el caso de uso |
| `services` | Lógica de negocio: normalizar, agregar pronóstico, cachear |
| `integrations` | Único módulo que conoce OpenWeatherMap (intercambiable) |
| `schemas` | DTOs Pydantic = contrato público |
| `core` | Configuración y manejo de errores |

**Frontend en capas:** `views` → `components` (presentación), `stores` (Pinia, estado),
`composables` (lógica reutilizable), `services` (axios → backend).

---

## Estructura

```
weather-app/
├── backend/              # API FastAPI (Python)
│   ├── app/
│   │   ├── api/          # routes + controllers + dependencies
│   │   ├── core/         # config + exceptions
│   │   ├── integrations/ # cliente OpenWeatherMap
│   │   ├── schemas/      # DTOs Pydantic
│   │   └── services/     # lógica de negocio
│   └── tests/
├── frontend/             # SPA Vue 3 (Vite + Tailwind)
│   └── src/
│       ├── components/   # SearchBar, CurrentWeatherCard, ForecastList...
│       ├── composables/  # useWeather
│       ├── services/     # weatherApi (axios)
│       ├── stores/       # Pinia
│       └── views/        # HomeView
└── docker-compose.yml    # orquestación opcional
```

---

## Stack

**Backend:** FastAPI · Uvicorn · httpx · Pydantic v2 · pydantic-settings · cachetools
· pytest + respx
**Frontend:** Vue 3 (Composition API) · Vite · Vue Router · Pinia · Axios · Tailwind CSS v4

---

## Requisitos

- **Python 3.11+** (backend)
- **Node.js 18+** (frontend)
- Una **API key gratuita** de OpenWeatherMap → https://openweathermap.org/api

---

## Puesta en marcha (manual)

### 1) Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt

Copy-Item .env.example .env      # luego edita .env y pon tu OWM_API_KEY
uvicorn app.main:app --reload
```

- API → http://127.0.0.1:8000
- Docs (Swagger) → http://127.0.0.1:8000/docs

### 2) Frontend (en otra terminal)

```powershell
cd frontend
npm install
npm run dev
```

- App → http://localhost:5173

> El frontend usa `VITE_API_BASE_URL` (por defecto `http://localhost:8000/api`). Para
> cambiarla, copia `.env.example` a `.env` en `frontend/`.

---

## Puesta en marcha (Docker, opcional)

```powershell
# Requiere backend/.env con tu OWM_API_KEY
docker compose up --build
```

- Frontend → http://localhost:5173
- Backend → http://localhost:8000

---

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/health` | Estado del servicio |
| GET | `/api/weather?city=Bogota` | Clima actual + pronóstico |
| GET | `/api/weather/current?city=Bogota` | Solo clima actual |
| GET | `/api/weather/forecast?city=Bogota&days=5` | Solo pronóstico |

Parámetros: `city` (obligatorio), `units` (`metric`\|`imperial`), `lang` (def. `es`).

---

## Pruebas

```powershell
cd backend
pytest
```

Las pruebas no consumen la API real (mockean el HTTP con `respx`), así que no necesitan key.

---

## Notas

- La **API key vive solo en el backend** (`backend/.env`), nunca en el navegador.
- La capa `integrations/` está aislada: cambiar de proveedor (p. ej. a WeatherAPI.com)
  solo implica añadir otro cliente con la misma interfaz, sin tocar el resto.
