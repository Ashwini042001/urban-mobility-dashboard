import pandas as pd
import sqlite3

# ✅ Path to your CSV file (adjust if needed)
csv_path = r"C:\Users\Ashwini\urban-mobility-dashboard\data\raw\yellow-tripdata-2023-03.csv"

# ✅ Path to your SQLite database
db_path = r"C:\Users\Ashwini\urban-mobility-dashboard\db\nyc_mobility.db"

# ✅ Load the CSV (first 50,000 rows), handle memory warning
df = pd.read_csv(csv_path, low_memory=False).head(50000)

# ✅ Select and rename columns to match your trips table schema
df = df[[
    'tpep_pickup_datetime',
    'tpep_dropoff_datetime',
    'passenger_count',
    'trip_distance',
    'fare_amount',
    'tip_amount',
    'total_amount',
    'PULocationID',
    'DOLocationID'
]].rename(columns={
    'tpep_pickup_datetime': 'pickup_datetime',
    'tpep_dropoff_datetime': 'dropoff_datetime'
})

# ✅ Connect to the SQLite database
conn = sqlite3.connect(db_path)

# ✅ Load data into 'trips' table
df.to_sql('trips', conn, if_exists='append', index=False)

print(f"✅ Successfully loaded {len(df)} rows into 'trips' table.")
conn.close()
