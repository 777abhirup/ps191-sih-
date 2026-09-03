import os
import osmnx as ox
import geopandas as gpd

place_name = "Wayanad, Kerala, India"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

print("Downloading building footprints...")
buildings = ox.features_from_place(place_name, tags={"building": True})
buildings = buildings[buildings.geometry.type.isin(["Polygon", "MultiPolygon"])]
keep = [c for c in ["geometry", "building", "name"] if c in buildings.columns]
buildings = buildings[keep].reset_index(drop=True)
buildings.to_file(os.path.join(ROOT_DIR, "buildings.geojson"), driver="GeoJSON")
print(f"Saved {len(buildings)} building footprints")

print("Downloading road network...")
graph = ox.graph_from_place(place_name, network_type="drive")
nodes, roads = ox.graph_to_gdfs(graph)
keep = [c for c in ["geometry", "highway", "name", "oneway", "length"] if c in roads.columns]
roads = roads[keep].reset_index(drop=True)
roads.to_file(os.path.join(ROOT_DIR, "roads.geojson"), driver="GeoJSON")
print(f"Saved {len(roads)} road segments")
