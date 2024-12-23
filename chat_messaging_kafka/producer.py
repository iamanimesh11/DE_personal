from kafka import KafkaProducer
import json
from datetime import datetime

def producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers='172.19.165.234:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k :k.encode('utf-8')

        )
        print("Chat Producer started. Type messages to send ('exit' to quit):")
    except Exception as e:
        print(f"Error occured:{e}")
        exit()
    while True:
        user=input("enter ur username:")
        message = input(user+"'s Message: ")
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if message.lower() == 'exit':
            break
        try:
            f=producer.send('chat-messages', key=user,value={'user': user, 'message': message,'timestamp':timestamp})
            f.get(timeout=10)
            print("Message sent!")

        except Exception as e:
            print(f"failed to send message {e}")

    producer.close()


if __name__ == "__main__":
    producer()
