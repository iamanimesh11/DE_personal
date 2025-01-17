import time
import json
from kafka import KafkaProducer
import random

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['172.19.165.234:9092'],  # Replace with your Kafka broker address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Define sample delivery agents with initial coordinates
delivery_agents = [
    {'id': 'agent_1', 'lat': 28.7041, 'lon': 77.1025},  # Delhi
    {'id': 'agent_2', 'lat': 19.0760, 'lon': 72.8777},  # Mumbai
    {'id': 'agent_3', 'lat': 12.9716, 'lon': 77.5946}  # Bangalore
]


def generate_random_movement(coord):
    """Generate random movement for latitude and longitude."""
    coord['lat'] += random.uniform(-0.001, 0.001)
    coord['lon'] += random.uniform(-0.001, 0.001)
    return coord


# Continuously send location updates
while True:
    for agent in delivery_agents:
        updated_location = generate_random_movement(agent)
        producer.send('location_updates', updated_location)
        print(f"Sent location update: {updated_location}")

    time.sleep(2)  # Simulate updates every 2 seconds
