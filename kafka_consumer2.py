from kafka import KafkaConsumer
import logging


consumer = KafkaConsumer(
    'another_topic',
    bootstrap_servers='172.19.165.234:9092',
    auto_offset_reset='earliest',  # Start from the beginning of the topic
    enable_auto_commit=True,
    group_id='python-consumer-group'
)

print("Starting to consume messages:")
for message in consumer:
        try:
            n=int(message.value.decode('utf-8'))
            print(f"n: {n}")
            if n %2!=0:
                print(f"Received: {message.value.decode('utf-8')}")
        except Exception as e:
          print(f"Error: {e}")
