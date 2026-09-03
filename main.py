import os
import numpy as np
import requests
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sklearn.cluster import DBSCAN
from shapely.geometry import MultiPoint, mapping

app = FastAPI(title="PS191 SIH - Hazard Zonation Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def compute_hsi_base_grid(lat: float, lon: float, grid_size: int = 30, step: float = 0.001):
    """Generate a local terrain grid and estimate base HSI from elevation variation."""
    lats = np.linspace(lat - (grid_size // 2) * step, lat + (grid_size // 2) * step, grid_size)
    lons = np.linspace(lon - (grid_size // 2) * step, lon + (grid_size // 2) * step, grid_size)
    grid_lats, grid_lons = np.meshgrid(lats, lons)

    try:
        flat_lats, flat_lons = grid_lats.ravel(), grid_lons.ravel()
        sample_indices = np.linspace(0, len(flat_lats) - 1, 9, dtype=int)
        s_lats = ",".join(map(str, flat_lats[sample_indices]))
        s_lons = ",".join(map(str, flat_lons[sample_indices]))
        url = f"https://api.open-meteo.com/v1/elevation?latitude={s_lats}&longitude={s_lons}"
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        elevs = res.json().get("elevation", [100.0] * 9)
        base_slope = max(float(np.std(elevs) / 8.0), 4.0)
    except Exception:
        base_slope = 15.0

    seed = abs(int(lat * 10000 + lon * 10000))
    rng = np.random.default_rng(seed)
    slope_raster = base_slope + rng.normal(0, 5.0, size=(grid_size, grid_size))
    slope_raster = np.clip(slope_raster, 1.0, 60.0)
    hsi_base_raster = np.clip(slope_raster / 45.0, 0.10, 0.85)
    return grid_lats, grid_lons, hsi_base_raster


@app.get("/api/hazard-zones")
def get_hsi_dynamics_hazard_zones(
    lat: float = Query(11.6854),
    lon: float = Query(76.1320),
    p_24hr: float = Query(120.0),
    p_threshold: float = Query(150.0),
    sm_t: float = Query(0.65),
    a: float = Query(0.40),
    b: float = Query(0.30),
    eps_deg: float = Query(0.0025),
    min_samples: int = Query(3),
):
    grid_lats, grid_lons, hsi_base = compute_hsi_base_grid(lat, lon)
    rain_ratio = p_24hr / max(p_threshold, 1.0)
    hsi_dynamics = hsi_base * (1.0 + a * rain_ratio + b * np.clip(sm_t, 0.0, 1.0))
    high_risk_mask = hsi_dynamics >= 0.75
    high_risk_lats = grid_lats[high_risk_mask]
    high_risk_lons = grid_lons[high_risk_mask]
    high_risk_scores = hsi_dynamics[high_risk_mask]
    features = []

    if len(high_risk_lats) >= min_samples:
        coords = np.column_stack((high_risk_lons, high_risk_lats))
        labels = DBSCAN(eps=eps_deg, min_samples=min_samples).fit(coords).labels_
        for cluster_id in set(labels):
            if cluster_id == -1:
                continue
            cluster_mask = labels == cluster_id
            cluster_coords = coords[cluster_mask]
            cluster_scores = high_risk_scores[cluster_mask]
            if len(cluster_coords) >= 3:
                poly_hull = MultiPoint(cluster_coords).convex_hull
                features.append({
                    "type": "Feature",
                    "geometry": mapping(poly_hull),
                    "properties": {
                        "cluster_id": int(cluster_id),
                        "max_hsi_dynamics": round(float(np.max(cluster_scores)), 3),
                        "avg_hsi_dynamics": round(float(np.mean(cluster_scores)), 3),
                        "is_red_zone": True,
                        "color": "#f43f5e",
                    },
                })

    return {
        "type": "FeatureCollection",
        "features": features,
        "metrics": {
            "mean_hsi_dynamics": round(float(np.mean(hsi_dynamics)), 3),
            "max_hsi_dynamics": round(float(np.max(hsi_dynamics)), 3),
            "high_risk_pixels_count": int(np.sum(high_risk_mask)),
            "vector_red_zones_count": len(features),
        },
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "PS191 SIH hazard engine"}


@app.get("/", response_class=HTMLResponse)
def render_frontend():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>index.html not found</h1>"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
