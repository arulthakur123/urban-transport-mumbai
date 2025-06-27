# step6a_convert_hotspots.py
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load CSV
df = pd.read_csv("ride_sharing_hotspots.csv")

# Convert to GeoDataFrame
geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Save as GeoJSON
gdf.to_file("ride_sharing_hotspots.geojson", driver="GeoJSON")

print("✅ Saved as ride_sharing_hotspots.geojson")
