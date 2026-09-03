import os
import geopandas as gpd
import h3
from rasterstats import zonal_stats
from shapely.geometry import Polygon

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SLOPE_PATH = os.path.join(SCRIPT_DIR, "static", "slope.tif")
BUILDINGS_PATH = os.path.join(SCRIPT_DIR, "buildings.geojson")
OUTPUT_GRID_PATH = os.path.join(SCRIPT_DIR, "spatial_grid.geojson")

bbox = [76.05, 11.45, 76.15, 11.55]
H3_RESOLUTION = 9

h3_poly = h3.LatLngPoly([
    (bbox[1], bbox[0]),
    (bbox[3], bbox[0]),
    (bbox[3], bbox[2]),
    (bbox[1], bbox[2]),
])

hexagons = list(h3.polygon_to_cells(h3_poly, res=H3_RESOLUTION))
hex_polygons = []
for h in hexagons:
    boundary = h3.cell_to_boundary(h)
    shape = Polygon([(p[1], p[0]) for p in boundary])
    hex_polygons.append({"hex_id": h, "geometry": shape})

grid_gdf = gpd.GeoDataFrame(hex_polygons, crs="EPSG:4326")

if os.path.exists(SLOPE_PATH):
    slope_stats = zonal_stats(grid_gdf, SLOPE_PATH, stats=["mean", "max"])
    grid_gdf["mean_slope"] = [s["mean"] or 0 for s in slope_stats]
    grid_gdf["max_slope"] = [s["max"] or 0 for s in slope_stats]
else:
    grid_gdf["mean_slope"] = 0.0
    grid_gdf["max_slope"] = 0.0

if os.path.exists(BUILDINGS_PATH):
    buildings = gpd.read_file(BUILDINGS_PATH)
    if buildings.crs != grid_gdf.crs:
        buildings = buildings.to_crs(grid_gdf.crs)
    joined = gpd.sjoin(buildings, grid_gdf, how="inner", predicate="intersects")
    building_counts = joined.groupby("hex_id").size().to_dict()
    grid_gdf["building_count"] = grid_gdf["hex_id"].map(building_counts).fillna(0)
else:
    grid_gdf["building_count"] = 0

grid_gdf["HSI_score"] = (
    (grid_gdf["mean_slope"] / 45.0) * 0.7
    + (grid_gdf["building_count"] / 100.0) * 0.3
).clip(0, 1)

grid_gdf.to_file(OUTPUT_GRID_PATH, driver="GeoJSON")
print(f"Generated unified spatial grid with {len(grid_gdf)} cells: {OUTPUT_GRID_PATH}")
