import sqlite3

# Connect to existing database
conn = sqlite3.connect("db/nyc_mobility.db")
cursor = conn.cursor()

# Create 'zones' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS zones (
    LocationID INTEGER PRIMARY KEY,
    Borough TEXT,
    Zone TEXT,
    service_zone TEXT
)
""")

# Create 'trips' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS trips (
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pickup_datetime TEXT,
    dropoff_datetime TEXT,
    passenger_count INTEGER,
    trip_distance REAL,
    fare_amount REAL,
    tip_amount REAL,
    total_amount REAL,
    PULocationID INTEGER,
    DOLocationID INTEGER,
    FOREIGN KEY(PULocationID) REFERENCES zones(LocationID),
    FOREIGN KEY(DOLocationID) REFERENCES zones(LocationID)
)
""")

conn.commit()
print("✅ Tables 'zones' and 'trips' created successfully.")
conn.close()
