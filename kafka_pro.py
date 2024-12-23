import json
import time

from kafka import KafkaProducer

# Create a producer instance

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')

)
traffic_Data = [
    {"sensor_id": "301", "location": "A", "traffic_level": "high"},
    {"sensor_id": "302", "location": "b", "traffic_level": "medium"},
    {"sensor_id": "303", "location": "c", "traffic_level": "low"}
]
for data in traffic_Data:
    future = producer.send('traffic-monitoring', data)
    try:
        record_metadata = future.get(timeout=10)  # Blocks until acknowledged
        print(f"Produced to topic {record_metadata.topic}, partition {record_metadata.partition}, offset {record_metadata.offset}")
    except Exception as e:
        print(f"Failed to send message: {e}")
    time.sleep(5)
time.sleep(100)
producer.close()

