import pandas as pd
import sqlite3

# Connect to DB
conn = sqlite3.connect(r"C:\Users\Ashwini\urban-mobility-dashboard\db\nyc_mobility.db")

# Load the trips table into a DataFrame
query = "SELECT * FROM trips"
df = pd.read_sql(query, conn)

conn.close()

# Preview the data
print("✅ DataFrame loaded:")
print(df.head())
print("\n📊 DataFrame info:")
print(df.info())
