import os
import numpy as np
import rasterio
from rasterio.transform import from_origin

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
dem_path = os.path.join(SCRIPT_DIR, "dem.tif")
slope_path = os.path.join(SCRIPT_DIR, "slope.tif")

x = np.linspace(0, 10, 100)
y = np.linspace(0, 10, 100)
X, Y = np.meshgrid(x, y)
elevation_data = (np.sin(X) + np.cos(Y)) * 500 + 1000

transform = from_origin(76.05, 11.55, 0.0003, 0.0003)
profile = {
    "driver": "GTiff",
    "height": elevation_data.shape[0],
    "width": elevation_data.shape[1],
    "count": 1,
    "dtype": rasterio.float32,
    "crs": "EPSG:4326",
    "transform": transform,
}

with rasterio.open(dem_path, "w", **profile) as dst:
    dst.write(elevation_data.astype(rasterio.float32), 1)

print("Created static/dem.tif")

dy, dx = np.gradient(elevation_data, 30, 30)
slope_deg = np.degrees(np.arctan(np.sqrt(dx**2 + dy**2)))

with rasterio.open(slope_path, "w", **profile) as dst:
    dst.write(slope_deg.astype(rasterio.float32), 1)

print("Created static/slope.tif")
