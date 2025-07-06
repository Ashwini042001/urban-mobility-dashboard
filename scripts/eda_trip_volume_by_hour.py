import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Set Seaborn style
sns.set_style("whitegrid")

# Load data from SQLite
conn = sqlite3.connect(r"C:\Users\Ashwini\urban-mobility-dashboard\db\nyc_mobility.db")
df = pd.read_sql("SELECT pickup_datetime FROM trips", conn)
conn.close()

# Convert pickup_datetime to datetime
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])

# Extract hour
df['hour'] = df['pickup_datetime'].dt.hour

# Count trips per hour
trip_counts = df['hour'].value_counts().sort_index()

# Plot with Seaborn
plt.figure(figsize=(12, 6))
sns.barplot(x=trip_counts.index, y=trip_counts.values, palette="Blues_d")
plt.title("🕒 NYC Yellow Taxi Trips by Hour of Day", fontsize=16)
plt.xlabel("Hour of Day", fontsize=14)
plt.ylabel("Number of Trips", fontsize=14)
plt.xticks(rotation=0)
plt.tight_layout()

plt.show()
