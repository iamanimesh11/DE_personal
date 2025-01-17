import sqlite3

conn = sqlite3.connect('locations.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM locations")
rows = cursor.fetchall()

for row in rows:
    print(row)
