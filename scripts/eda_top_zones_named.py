import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

sns.set_style("whitegrid")

# Load the zone lookup CSV
lookup_path = r"C:\Users\Ashwini\urban-mobility-dashboard\data\lookup\taxi_zone_lookup.csv"
zone_lookup = pd.read_csv(lookup_path)

# Connect to DB
conn = sqlite3.connect(r"C:\Users\Ashwini\urban-mobility-dashboard\db\nyc_mobility.db")

# Load pickup counts
pickup_query = """
SELECT PULocationID as location_id, COUNT(*) as trip_count
FROM trips
GROUP BY PULocationID
ORDER BY trip_count DESC
LIMIT 10
"""
df_pickup = pd.read_sql(pickup_query, conn)

# Load dropoff counts
dropoff_query = """
SELECT DOLocationID as location_id, COUNT(*) as trip_count
FROM trips
GROUP BY DOLocationID
ORDER BY trip_count DESC
LIMIT 10
"""
df_dropoff = pd.read_sql(dropoff_query, conn)

conn.close()

# Merge with lookup to get zone names
df_pickup_named = df_pickup.merge(zone_lookup[['LocationID', 'Zone']], left_on='location_id', right_on='LocationID', how='left')
df_dropoff_named = df_dropoff.merge(zone_lookup[['LocationID', 'Zone']], left_on='location_id', right_on='LocationID', how='left')

# Plot top 10 pickups with zone names
plt.figure(figsize=(14, 6))
sns.barplot(data=df_pickup_named, x='Zone', y='trip_count', palette='Blues_d')
plt.title("📍 Top 10 Pickup Zones by Trip Count", fontsize=16)
plt.xlabel("Zone", fontsize=14)
plt.ylabel("Number of Trips", fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot top 10 dropoffs with zone names
plt.figure(figsize=(14, 6))
sns.barplot(data=df_dropoff_named, x='Zone', y='trip_count', palette='Greens_d')
plt.title("📍 Top 10 Dropoff Zones by Trip Count", fontsize=16)
plt.xlabel("Zone", fontsize=14)
plt.ylabel("Number of Trips", fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
