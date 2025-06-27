import pandas as pd

df_density = pd.read_csv("zone_transit_density.csv")
df_ridership = pd.read_csv("transport_mumbai_data/zone_wise_ridership.csv")

print("📌 Density CSV columns:", df_density.columns.tolist())
print("📌 Ridership CSV columns:", df_ridership.columns.tolist())
