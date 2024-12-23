from kafka import KafkaProducer
import json

def producer():
    producer = KafkaProducer(
        bootstrap_servers='172.19.165.234:9092',
        key_serializer=lambda k: k.encode('utf-8'),  # Serialize the key
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize the value
    )
    print("Chat Producer started. Type messages to send ('exit' to quit):")

    while True:
        user = input("Enter username (User1/User2): ")
        if user.lower() == 'exit':
            break
        message = input(f"{user}: ")
        producer.send('chat-messagessss', key=user, value={'user': user, 'message': message})
        print("Message sent!")

    producer.close()

if __name__ == "__main__":
    producer()