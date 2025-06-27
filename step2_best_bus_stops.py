import requests
import pandas as pd
import json

# Overpass API URL
overpass_url = "http://overpass-api.de/api/interpreter"

# Query for BEST bus stops in Mumbai
query = """
[out:json][timeout:50];
area["name"="Mumbai Metropolitan Region"]->.searchArea;
node["highway"="bus_stop"](area.searchArea);
out body;
"""

print("⏳ Querying Overpass API for BEST bus stops...")
response = requests.get(overpass_url, params={'data': query})

if response.status_code != 200:
    print("❌ Failed to fetch data from Overpass API.")
    exit()

data = response.json()

# Parse node data
bus_stops = []
for element in data['elements']:
    bus_stop = {
        "id": element['id'],
        "name": element['tags'].get('name', 'Unnamed'),
        "lat": element['lat'],
        "lon": element['lon']
    }
    bus_stops.append(bus_stop)

# Create DataFrame
df = pd.DataFrame(bus_stops)

# Save as CSV
df.to_csv("best_bus_stops_mumbai.csv", index=False)
print("✅ Saved BEST bus stop data as best_bus_stops_mumbai.csv")

# Optional GeoJSON
try:
    import geopandas as gpd
    from shapely.geometry import Point

    df['geometry'] = df.apply(lambda row: Point(row['lon'], row['lat']), axis=1)
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")
    gdf.to_file("best_bus_stops_mumbai.geojson", driver="GeoJSON")
    print("🗺️ Saved as best_bus_stops_mumbai.geojson (GeoJSON format)")
except ImportError:
    print("⚠️ GeoPandas not installed, skipping GeoJSON export.")
