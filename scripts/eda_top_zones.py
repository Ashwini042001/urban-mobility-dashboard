import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

sns.set_style("whitegrid")

# Connect and load pickup & dropoff location counts
conn = sqlite3.connect(r"C:\Users\Ashwini\urban-mobility-dashboard\db\nyc_mobility.db")
pickup_query = """
SELECT PULocationID as location_id, COUNT(*) as trip_count
FROM trips
GROUP BY PULocationID
ORDER BY trip_count DESC
LIMIT 10
"""
dropoff_query = """
SELECT DOLocationID as location_id, COUNT(*) as trip_count
FROM trips
GROUP BY DOLocationID
ORDER BY trip_count DESC
LIMIT 10
"""

df_pickup = pd.read_sql(pickup_query, conn)
df_dropoff = pd.read_sql(dropoff_query, conn)
conn.close()

# Plot top 10 pickups
plt.figure(figsize=(14, 6))
sns.barplot(data=df_pickup, x='location_id', y='trip_count', palette='Blues_d')
plt.title("📍 Top 10 Pickup Locations by Trip Count", fontsize=16)
plt.xlabel("Location ID", fontsize=14)
plt.ylabel("Number of Trips", fontsize=14)
plt.tight_layout()
plt.show()

# Plot top 10 dropoffs
plt.figure(figsize=(14, 6))
sns.barplot(data=df_dropoff, x='location_id', y='trip_count', palette='Greens_d')
plt.title("📍 Top 10 Dropoff Locations by Trip Count", fontsize=16)
plt.xlabel("Location ID", fontsize=14)
plt.ylabel("Number of Trips", fontsize=14)
plt.tight_layout()
plt.show()
