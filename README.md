# PS191 SIH — Hazard Zonation & Safe-Zone Platform

A prototype disaster-intelligence web application for dynamic hazard assessment, carrying-capacity analysis, and relocation planning.

## Included

- Frontend: `index.html`, `app.js`, `styles.css`
- FastAPI backend: `main.py`
- Dynamic HSI API: `/api/hazard-zones`
- Health check: `/health`
- GIS preprocessing: `grid_system.py`
- Terrain generator: `static/slope.py`
- OpenStreetMap building/road generator: `static/Building and Roads.py`
- Dependencies: `requirements.txt`
- Docker: `Dockerfile` and `docker-compose.yml`

The frontend uses Leaflet/OpenStreetMap for the map and Open-Meteo for live weather data. It also has an offline illustrative fallback so the dashboard remains viewable if the weather API is unavailable.

## Run locally

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
pip install -r requirements.txt
```

Windows PowerShell activation:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start the application:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`.

## Docker

```bash
docker compose up --build
```

Then open `http://localhost:8000`.

## Optional GIS preprocessing

The GIS scripts can generate the terrain and OpenStreetMap datasets:

```bash
python static/slope.py
python "static/Building and Roads.py"
python grid_system.py
```

The generated GeoTIFF and large GeoJSON datasets are intentionally not committed to this lightweight repository. Generate them locally when the GIS preprocessing workflow needs them.

## Backend API

Example:

```text
GET /api/hazard-zones?lat=11.6854&lon=76.1320&p_24hr=120&p_threshold=150&sm_t=0.65
```

The endpoint builds a local terrain grid, calculates dynamic HSI, thresholds cells at HSI >= 0.75, clusters high-risk cells with DBSCAN, and returns red-zone polygons as GeoJSON.

## Structure

```text
ps191-sih-/
├── index.html
├── app.js
├── styles.css
├── main.py
├── grid_system.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── README.md
└── static/
    ├── slope.py
    └── Building and Roads.py
```

## Important prototype note

Hazard coefficients, demographic values, safe-zone capacities, and some dashboard values are illustrative. Replace them with validated local GIS, sensor, hydrology, geotechnical, shelter, and demographic datasets before operational use.

Attribution: the backend/GIS workflow was adapted from the public prototype `sooryadarshch/Hackathon`, while the current frontend is the Codex-generated SafeZone dashboard.
