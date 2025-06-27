import os
import geopandas as gpd
import osmnx as ox

# Ensure output folder exists
os.makedirs("transport_mumbai_data", exist_ok=True)

print("⏳ Fetching ward-level boundaries from OpenStreetMap...")

# Use the older function name compatible with your version
gdf = ox.features_from_place("Mumbai, India", tags={"boundary": "administrative", "admin_level": "10"})

# Keep only name and geometry columns, and drop missing values
gdf = gdf[["name", "geometry"]].dropna()
gdf = gdf[~gdf["name"].duplicated()]  # remove duplicates

# Save as GeoJSON
gdf.to_file("transport_mumbai_data/mumbai_wards.geojson", driver="GeoJSON")
print("✅ Saved ward-level boundaries as mumbai_wards.geojson")
import osmnx as ox
import geopandas as gpd

# 🗺️ Fetch ward-level administrative boundaries (admin_level=10)
print("⏳ Fetching ward-level boundaries from OSM...")
gdf = ox.features_from_place("Mumbai, India", tags={
    "boundary": "administrative",
    "admin_level": "10"
})

# 🧹 Keep only polygons and clean
gdf = gdf[gdf.geometry.type.isin(["Polygon", "MultiPolygon"])].copy()
gdf = gdf[["name", "geometry"]]
gdf = gdf.dropna(subset=["name"])

# 💾 Save to GeoJSON
gdf.to_file("transport_mumbai_data/mumbai_wards.geojson", driver="GeoJSON")
print("✅ Saved: transport_mumbai_data/mumbai_wards.geojson")
