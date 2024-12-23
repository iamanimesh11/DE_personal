from kafka import KafkaConsumer, TopicPartition
import json


def consumer2():
    consumer = KafkaConsumer(
        bootstrap_servers='172.19.165.234:9092',  # Replace with your Kafka server
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        enable_auto_commit=False , # Disable auto commit to handle offsets manually

    )

    # Assign specific partition (Partition 0 for Consumer 1)
    partition = TopicPartition('chat-messages', 1)
    consumer.assign([partition])

    print("Chat Consumer 1 started. Listening for messages on Partition 0:")

    for message in consumer:
        data = message.value
        print(f"{data['user']} : {data['message']}  {data['timestamp']}")


if __name__ == "__main__":
    consumer2()