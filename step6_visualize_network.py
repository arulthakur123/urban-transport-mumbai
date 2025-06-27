# step6_visualize_network.py

import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt

# Load road network
G = ox.load_graphml("transport_mumbai_data/mumbai_road_network.graphml")

# Load metro, bus, and ride-sharing GeoJSONs
gdf_metro = gpd.read_file("metro_stations_mumbai.geojson")
gdf_bus = gpd.read_file("best_bus_stops_mumbai.geojson")
gdf_hotspots = gpd.read_file("ride_sharing_hotspots.geojson")

# Plotting
fig, ax = plt.subplots(figsize=(14, 14))

# Plot road network
ox.plot_graph(G, ax=ax, show=False, close=False, edge_color='gray', node_size=0, edge_linewidth=0.3)

# Plot transit locations
gdf_metro.plot(ax=ax, color='red', markersize=20, label='Metro Stations')
gdf_bus.plot(ax=ax, color='blue', markersize=20, label='Bus Stops')
gdf_hotspots.plot(ax=ax, color='green', markersize=20, label='Ride-share Hotspots')

# Add legend and title
plt.legend()
plt.title("Mumbai Urban Transit Network", fontsize=16)
plt.tight_layout()

# Save output
plt.savefig("fig_mumbai_transit_network.png", dpi=300)
print("✅ Transit network visual saved as fig_mumbai_transit_network.png")
