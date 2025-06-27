# step5_spatial_join.py

import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim
from shapely.geometry import Point
import time

# 📥 Load transit ridership data
print("📥 Loading ridership data...")
df_rider = pd.read_csv("transport_mumbai_data/transit_ridership.csv")
print("✅ Loaded:", df_rider.shape)

# 🌐 Geocoder initialization
geolocator = Nominatim(user_agent="mumbai_transit_geocoder")

def geocode_location(place):
    try:
        location = geolocator.geocode(f"{place}, Mumbai, India")
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except:
        return None, None

# 📍 Geocode stops
print("📍 Geocoding transit stops...")
df_rider['lat'], df_rider['lon'] = zip(*df_rider['Transit_Stop'].apply(lambda x: geocode_location(x)))
df_rider = df_rider.dropna(subset=['lat', 'lon'])
print(f"📌 Geocoded: {df_rider.shape[0]} stops")

# 🌍 Convert to GeoDataFrame
geometry = [Point(xy) for xy in zip(df_rider['lon'], df_rider['lat'])]
gdf_rider = gpd.GeoDataFrame(df_rider, geometry=geometry, crs="EPSG:4326")

# 🗺️ Load ward-level boundaries
print("🗺️ Loading Mumbai wards...")
gdf_zones = gpd.read_file("transport_mumbai_data/mumbai_wards.geojson")

# 🔗 Spatial join: assign each stop to a ward
print("🔗 Performing spatial join...")
gdf_joined = gpd.sjoin(gdf_rider, gdf_zones, how="left", predicate="intersects")
print("📋 Joined columns:", list(gdf_joined.columns))

# 🧮 Group by ward and sum ridership
zone_col = "name" if "name" in gdf_zones.columns else gdf_zones.columns[-1]  # fallback for ward name column
zone_ridership = gdf_joined.groupby(zone_col)['Avg_Daily_Ridership'].sum().reset_index()
zone_ridership.columns = ["name", "Avg_Daily_Ridership"]

# 💾 Save final mapping
zone_ridership.to_csv("transport_mumbai_data/zone_wise_ridership.csv", index=False)
print("✅ Saved zone-wise ridership as zone_wise_ridership.csv")
