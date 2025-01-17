from kafka import KafkaConsumer
import sqlite3
import json

# Kafka Consumer Configuration
consumer = KafkaConsumer('location-tracking',
                         bootstrap_servers='172.19.165.234:9092',
                         group_id='location-consumer-group',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Initialize SQLite database
conn = sqlite3.connect('locations.db')
cursor = conn.cursor()

# Create the locations table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS locations (
    id TEXT,
    latitude REAL,
    longitude REAL,
    timestamp REAL
)
""")
conn.commit()

# Process messages from Kafka
for message in consumer:
    location = message.value  # Get the location data from the Kafka message
    print(f"Consumed: {location}")

    # Store the location data in the database
    cursor.execute("""
    INSERT INTO locations (id, latitude, longitude, timestamp) 
    VALUES (?, ?, ?, ?)
    """, (location['id'], location['latitude'], location['longitude'], location['timestamp']))
    conn.commit()
