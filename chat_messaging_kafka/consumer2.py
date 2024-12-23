from kafka import KafkaConsumer
import json


def consumer1():
    consumer = KafkaConsumer(
        'chat-messages',
        bootstrap_servers='172.19.165.234:9092',
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        group_id='chat-group'
    )
    print("Chat Consumer 1 started. Listening for messages:")

    for message in consumer:
        data = message.value
        key=message.key.decode('utf-8') if message.key else 'None'
        # print(f"{data['user']}: {data['message']} - {data['timestamp']}")
        print(f"{key}:{data['message']}")



if __name__ == "__main__":
    consumer1()
