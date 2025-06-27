# step3_route_mapping.py

import geopandas as gpd
import pandas as pd
import networkx as nx
import osmnx as ox
import folium
import matplotlib.pyplot as plt

# Load GeoJSON & CSV data
gdf_metro = gpd.read_file("metro_stations_mumbai.geojson")
gdf_bus = gpd.read_file("best_bus_stops_mumbai.geojson")
gdf_admin = gpd.read_file("transport_mumbai_data/mumbai_admin_boundaries.geojson")
road_graph = ox.load_graphml("transport_mumbai_data/mumbai_road_network.graphml")
df_rideshare = pd.read_csv("ride_sharing_hotspots.csv")

# Convert ride-sharing CSV to GeoDataFrame
gdf_rideshare = gpd.GeoDataFrame(df_rideshare,
                                  geometry=gpd.points_from_xy(df_rideshare.Longitude, df_rideshare.Latitude),
                                  crs="EPSG:4326")

# ---------------------- STATIC MAP ----------------------
fig, ax = plt.subplots(figsize=(12, 12))
gdf_admin.plot(ax=ax, color='whitesmoke', edgecolor='black', alpha=0.5)

# Plot all layers
gdf_metro.plot(ax=ax, color='red', markersize=30, label='Metro Stations')
gdf_bus.plot(ax=ax, color='blue', markersize=20, label='BEST Bus Stops')
gdf_rideshare.plot(ax=ax, color='green', markersize=20, label='Ride-Sharing Hotspots')

# Plot road network
ox.plot_graph(road_graph, ax=ax, node_size=0, edge_color='gray', edge_linewidth=0.5, show=False, close=False)

plt.legend()
plt.title("🗺️ Mumbai Public Transport Network", fontsize=14)
plt.axis('off')
plt.tight_layout()
plt.savefig("transport_map_static.png")
print("✅ Saved static transport map as 'transport_map_static.png'")

# ---------------------- INTERACTIVE MAP ----------------------
# Base map centered at Mumbai
mumbai_center = [19.0760, 72.8777]
map_folium = folium.Map(location=mumbai_center, zoom_start=11)

# Add Metro stations
for _, row in gdf_metro.iterrows():
    folium.CircleMarker(location=[row.geometry.y, row.geometry.x],
                        radius=4, color='red', fill=True, popup=row['name']).add_to(map_folium)

# Add Bus stops
for _, row in gdf_bus.iterrows():
    folium.CircleMarker(location=[row.geometry.y, row.geometry.x],
                        radius=2, color='blue', fill=True).add_to(map_folium)

# Add Ride-share hotspots
for _, row in gdf_rideshare.iterrows():
    folium.Marker(location=[row.geometry.y, row.geometry.x],
                  popup=row['Name'],
                  icon=folium.Icon(color='green', icon='taxi', prefix='fa')).add_to(map_folium)

# Save interactive map
map_folium.save("transport_map_interactive.html")
print("✅ Saved interactive map as 'transport_map_interactive.html'")

