import sqlite3

# ✅ Connect to the SQLite DB
conn = sqlite3.connect(r"C:\Users\Ashwini\urban-mobility-dashboard\db\nyc_mobility.db")
cursor = conn.cursor()

# 1. Count total trips
cursor.execute("SELECT COUNT(*) FROM trips;")
row_count = cursor.fetchone()[0]
print(f"🧾 Total trips loaded: {row_count}")

# 2. Print 5 sample trips
print("\n📌 Sample 5 trips:")
cursor.execute("SELECT * FROM trips LIMIT 5;")
for row in cursor.fetchall():
    print(row)

# 3. Show top 5 most common pickup locations
print("\n📍 Top 5 pickup locations (LocationID):")
cursor.execute("""
    SELECT PULocationID, COUNT(*) as trip_count
    FROM trips
    WHERE PULocationID IS NOT NULL
    GROUP BY PULocationID
    ORDER BY trip_count DESC
    LIMIT 5;
""")
results = cursor.fetchall()

if results:
    for loc in results:
        print(f"LocationID: {loc[0]}, Trips: {loc[1]}")
else:
    print("❌ No pickup data found.")

# ✅ Close the connection
conn.close()
print("\n✅ Verification complete.")
