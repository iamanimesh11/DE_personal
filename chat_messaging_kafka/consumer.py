from kafka import KafkaConsumer
import json
from kafka import TopicPartition

def consumer1():
    consumer = KafkaConsumer(
        'chat-messages',
        bootstrap_servers='172.19.165.234:9092',
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        # group_id='chat-group',#set to none for manual partitial assignment
        group_id=None,  # set to none for manual partitial assignment
        enable_auto_commit = False  # Disable auto commit

    )
    print("Chat Consumer 1 started. Listening for messages:")
    partition=
    for message in consumer:
        data = message.value
        key=message.key.decode('utf-8') if message.key else 'None'
        # print(f"{data['user']}: {data['message']} - {data['timestamp']}")
        print(f"{key}:{data['message']}")



if __name__ == "__main__":
    consumer1()
