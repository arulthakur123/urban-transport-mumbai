import overpy
import csv

api = overpy.Overpass()

# Define the bounding box for Mumbai: (south, west, north, east)
bbox = "19.0,72.77,19.3,72.97"

# Define hotspot queries
queries = {
    "Airport Terminal": f'node["aeroway"="terminal"]({bbox});',
    "Railway Station": f'node["railway"="station"]({bbox});',
    "Bus Station": f'node["amenity"="bus_station"]({bbox});',
    "Mall": f'node["shop"="mall"]({bbox});',
    "Office": f'node["office"]({bbox});',
    "Taxi Stand": f'node["amenity"="taxi"]({bbox});'
}

# Collect results
all_hotspots = []

print("⏳ Querying Overpass API for ride-sharing hotspots in Mumbai...\n")

for category, query in queries.items():
    full_query = f"[out:json];{query}out;"
    try:
        result = api.query(full_query)
        for node in result.nodes:
            name = node.tags.get("name", "Unnamed")
            lat = node.lat
            lon = node.lon
            all_hotspots.append([category, name, lat, lon])
        print(f"✅ Found {len(result.nodes)} results for: {category}")
    except Exception as e:
        print(f"❌ Failed to fetch {category}: {e}")

# Save to CSV
output_file = "ride_sharing_hotspots.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Category", "Name", "Latitude", "Longitude"])
    writer.writerows(all_hotspots)

print(f"\n📄 Saved all hotspot data to: {output_file}")
