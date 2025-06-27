import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load administrative boundaries
gdf_admin = gpd.read_file("transport_mumbai_data/mumbai_admin_boundaries.geojson")

# Load population data
df_pop = pd.read_csv("transport_mumbai_data/population_density.csv")

# Load ridership data
df_ride = pd.read_csv("transport_mumbai_data/transit_ridership.csv")

# Merge population with ridership data
df_merged = pd.merge(df_pop, df_ride, on="zone_id", how="inner")

# Merge with spatial boundary
gdf_merged = gdf_admin.merge(df_merged, on="zone_id")

# Calculate ridership per 1000 people
gdf_merged["riders_per_1000"] = (gdf_merged["daily_ridership"] / gdf_merged["population"]) * 1000

# Save merged data
gdf_merged.to_file("demand_by_zone.geojson", driver="GeoJSON")

# Visualization: Demand Heatmap
plt.figure(figsize=(12, 8))
gdf_merged.plot(column="riders_per_1000", cmap="OrRd", legend=True, edgecolor='black')
plt.title("📍 Transit Demand by Zone (Riders per 1000 People)", fontsize=15)
plt.axis('off')
plt.tight_layout()
plt.savefig("fig_demand_heatmap.png")
plt.show()

print("✅ Demand modeling complete. GeoJSON and PNG heatmap saved.")
