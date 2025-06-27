import osmnx as ox
import geopandas as gpd
import pandas as pd
import os
from shapely.geometry import Point

# Create folder to store the data
output_dir = "transport_mumbai_data"
os.makedirs(output_dir, exist_ok=True)

# 1. Mumbai Road Network
print("⏳ Downloading Mumbai road network...")
road_graph = ox.graph_from_place("Mumbai, India", network_type="drive")
ox.save_graphml(road_graph, filepath=f"{output_dir}/mumbai_road_network.graphml")
print("✅ Road network saved.")

# 2. Administrative Boundaries
print("⏳ Saving admin boundary as GeoJSON...")
gdf_admin = ox.geocode_to_gdf("Mumbai, India")
gdf_admin.to_file(f"{output_dir}/mumbai_admin_boundaries.geojson", driver='GeoJSON')
print("✅ Admin boundary saved.")

# 3. Simulated Population Density by Wards
population_density_data = {
    "Ward": ["A", "B", "C", "D", "E", "F North", "F South", "G North", "G South", "H East", "H West"],
    "Population_Density": [32000, 29000, 31000, 27000, 30000, 33000, 34000, 36000, 28000, 30000, 29000]
}
pd.DataFrame(population_density_data).to_csv(f"{output_dir}/population_density.csv", index=False)
print("✅ Population data saved.")

# 4. Simulated Transit Ridership
transit_ridership = {
    "Transit_Stop": ["Andheri", "Ghatkopar", "Dadar", "Kurla", "Bandra", "Churchgate", "Borivali", "CST"],
    "Avg_Daily_Ridership": [150000, 130000, 180000, 160000, 170000, 140000, 155000, 145000]
}
pd.DataFrame(transit_ridership).to_csv(f"{output_dir}/transit_ridership.csv", index=False)
print("✅ Ridership data saved.")

# 5. Simulated Fare Matrix
fare_matrix = {
    "Mode": ["Metro", "BEST Bus", "Auto", "Taxi"],
    "Base_Fare": [10, 5, 15, 25],
    "Per_KM_Rate": [2, 1.5, 12, 20]
}
pd.DataFrame(fare_matrix).to_csv(f"{output_dir}/fare_data.csv", index=False)
print("✅ Fare matrix saved.")

# 6. Simulated Traffic Zones
zones = gpd.GeoDataFrame({
    "Zone": ["Worli", "Sion", "Andheri", "Bandra"],
    "geometry": [
        Point(72.817, 18.994).buffer(0.01),
        Point(72.859, 19.038).buffer(0.01),
        Point(72.846, 19.119).buffer(0.01),
        Point(72.834, 19.055).buffer(0.01)
    ]
}, crs="EPSG:4326")
zones.to_file(f"{output_dir}/traffic_zones.geojson", driver="GeoJSON")
print("✅ Traffic zones saved.")
