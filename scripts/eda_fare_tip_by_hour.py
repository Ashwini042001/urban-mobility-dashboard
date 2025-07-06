import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

sns.set_style("whitegrid")

# Load necessary columns from DB
conn = sqlite3.connect(r"C:\Users\Ashwini\urban-mobility-dashboard\db\nyc_mobility.db")
query = """
SELECT pickup_datetime, fare_amount, tip_amount FROM trips
"""
df = pd.read_sql(query, conn)
conn.close()

# Convert pickup_datetime to datetime and extract hour
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
df['hour'] = df['pickup_datetime'].dt.hour

# Group by hour, calculate average fare and tip
hourly_stats = df.groupby('hour')[['fare_amount', 'tip_amount']].mean().reset_index()

# Plot
plt.figure(figsize=(12, 6))
sns.lineplot(data=hourly_stats, x='hour', y='fare_amount', marker='o', label='Avg Fare')
sns.lineplot(data=hourly_stats, x='hour', y='tip_amount', marker='o', label='Avg Tip')

plt.title("💰 Average Fare & Tip Amount by Hour of Day", fontsize=16)
plt.xlabel("Hour of Day", fontsize=14)
plt.ylabel("Amount ($)", fontsize=14)
plt.xticks(range(0, 24))
plt.legend()
plt.tight_layout()

plt.show()
