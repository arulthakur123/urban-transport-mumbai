import pandas as pd

# Load zone-wise transit stop density and ridership data
df_density = pd.read_csv("zone_transit_density.csv")
df_ridership = pd.read_csv("transport_mumbai_data/zone_wise_ridership.csv")

# Merge on correct key: 'name'
df_merged = pd.merge(df_density, df_ridership, on="name", how="outer")

# Fill missing values
df_merged["total_stops"] = df_merged["total_stops"].fillna(0)
df_merged["Avg_Daily_Ridership"] = df_merged["Avg_Daily_Ridership"].fillna(0)

# Calculate ridership per stop (avoid divide-by-zero)
df_merged["ridership_per_stop"] = df_merged.apply(
    lambda row: row["Avg_Daily_Ridership"] / row["total_stops"] if row["total_stops"] > 0 else 0,
    axis=1
)

# Identify underserved zones
underserved = df_merged[
    (df_merged["total_stops"] < df_merged["total_stops"].median()) &
    (df_merged["Avg_Daily_Ridership"] > df_merged["Avg_Daily_Ridership"].median())
]

# Identify overloaded zones
overloaded = df_merged[
    df_merged["ridership_per_stop"] > df_merged["ridership_per_stop"].quantile(0.75)
]

# Save insights
underserved.to_csv("insights_underserved_zones.csv", index=False)
overloaded.to_csv("insights_overloaded_stops.csv", index=False)

# Print summary
print("\n🔍 Urban Mobility Insights Summary")
print("--------------------------------------------------")
print(f"🚨 Underserved Zones: {len(underserved)}")
print(f"🔥 Overloaded Stops: {len(overloaded)}")
print("✅ Insights saved to: 'insights_underserved_zones.csv' & 'insights_overloaded_stops.csv'")
