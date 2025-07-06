import sqlite3
conn = sqlite3.connect("db/nyc_mobility.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM zones LIMIT 5")
print(cursor.fetchall())
conn.close()
