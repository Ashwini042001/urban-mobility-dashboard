import sqlite3
import os

# Step 1: Make sure 'db' folder exists
os.makedirs("db", exist_ok=True)

# Step 2: Create/connect to SQLite database file
conn = sqlite3.connect("db/nyc_mobility.db")
cursor = conn.cursor()

print("✅ SQLite database created at db/nyc_mobility.db")

# Step 3: Close connection
conn.close()
