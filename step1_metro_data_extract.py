import requests
import pandas as pd
import json

# Define the Overpass API URL
overpass_url = "http://overpass-api.de/api/interpreter"

# Query: Mumbai Metro station nodes tagged as railway=station + metro=yes
query = """
[out:json][timeout:50];
area["name"="Mumbai Metropolitan Region"]->.searchArea;
(
  node["railway"="station"]["station"="subway"](area.searchArea);
  node["railway"="station"]["station"="light_rail"](area.searchArea);
);
out body;
"""

print("⏳ Querying Overpass API for Mumbai Metro stations...")
response = requests.get(overpass_url, params={'data': query})

if response.status_code != 200:
    print("❌ Failed to fetch data from Overpass API.")
    exit()

data = response.json()

# Parse node data
stations = []
for element in data['elements']:
    station = {
        "id": element['id'],
        "name": element['tags'].get('name', 'Unnamed'),
        "lat": element['lat'],
        "lon": element['lon'],
        "operator": element['tags'].get('operator', 'Unknown'),
        "station_type": element['tags'].get('station', 'N/A')
    }
    stations.append(station)

# Create DataFrame
df = pd.DataFrame(stations)

# Save as CSV
df.to_csv("metro_stations_mumbai.csv", index=False)
print("✅ Saved metro station data as metro_stations_mumbai.csv")

# Optional: Save as GeoJSON (if using GeoPandas)
try:
    import geopandas as gpd
    from shapely.geometry import Point

    df['geometry'] = df.apply(lambda row: Point(row['lon'], row['lat']), axis=1)
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")
    gdf.to_file("metro_stations_mumbai.geojson", driver="GeoJSON")
    print("🗺️ Saved as metro_stations_mumbai.geojson (GeoJSON format)")
except ImportError:
    print("⚠️ GeoPandas not installed, skipping GeoJSON export.")
