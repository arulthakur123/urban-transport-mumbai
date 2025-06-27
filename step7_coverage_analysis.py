# step7_coverage_analysis.py

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from shapely.ops import nearest_points

print("📥 Loading data...")

gdf_zones = gpd.read_file("transport_mumbai_data/mumbai_wards.geojson")

gdf_metro = gpd.read_file("metro_stations_mumbai.geojson")
gdf_bus = gpd.read_file("best_bus_stops_mumbai.geojson")
gdf_hotspots = gpd.read_file("ride_sharing_hotspots.geojson")

# Ensure all layers have same CRS
gdf_zones = gdf_zones.to_crs(epsg=4326)
gdf_metro = gdf_metro.to_crs(epsg=4326)
gdf_bus = gdf_bus.to_crs(epsg=4326)
gdf_hotspots = gdf_hotspots.to_crs(epsg=4326)

print("🧮 Calculating transit stop density per zone...")

# Count stops per zone
gdf_metro["type"] = "metro"
gdf_bus["type"] = "bus"
gdf_all_stops = pd.concat([gdf_metro, gdf_bus], ignore_index=True)

gdf_joined = gpd.sjoin(gdf_all_stops, gdf_zones, predicate="within")
stop_counts = gdf_joined.groupby("name_right").size().reset_index(name="total_stops")



print("📏 Calculating average distance to nearest transit stop for ride-share hotspots...")

# Function to find nearest stop
def nearest_stop_distance(row, stops_gdf):
    nearest_geom = nearest_points(row.geometry, stops_gdf.unary_union)[1]
    return row.geometry.distance(nearest_geom)

gdf_hotspots["dist_to_transit"] = gdf_hotspots.apply(
    lambda row: nearest_stop_distance(row, gdf_all_stops), axis=1
)

avg_dist = gdf_hotspots["dist_to_transit"].mean()

print(f"📐 Average distance to nearest transit: {avg_dist:.4f} degrees (~{avg_dist*111:.2f} km)")

# Merge into zone level stats
gdf_zones_stats = gdf_zones.merge(stop_counts, how="left", left_on="name", right_on="name_right")

gdf_zones_stats["total_stops"].fillna(0, inplace=True)

gdf_zones_stats.to_file("mumbai_zone_coverage.geojson", driver="GeoJSON")
gdf_zones_stats[["name", "total_stops"]].to_csv("zone_transit_density.csv", index=False)

print("✅ Saved zone-wise transit density as 'zone_transit_density.csv'")
print("✅ Saved enriched zone GeoJSON as 'mumbai_zone_coverage.geojson'")
