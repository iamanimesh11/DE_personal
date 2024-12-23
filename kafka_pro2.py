import time

from kafka import KafkaProducer
import logging

producer = KafkaProducer(bootstrap_servers='172.19.165.234:9092')

try:
    for i in range(10):
        producer.send('another_topic', value=str(i).encode('utf-8'))
        print(i)
        time.sleep(5)

    producer.flush()
except Exception as e:
    print(f"Error: {e}")
finally:
    producer.close()
