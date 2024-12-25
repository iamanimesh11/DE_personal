import time

from kafka import KafkaProducer
import json
from datetime import datetime
from kafka.admin import KafkaAdminClient,NewTopic



import string
import random

# using random.choices() generating random strings
res = ''.join(random.choices(string.ascii_letters,
                             k=7)) # initializing size of string

print(str(res))


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
        while True:
            # user=input("enter ur username:").strip()
            # user=# using random.choices() generating random strings
            user= ''.join(random.choices(string.ascii_letters, k=7)) # initializing size of string
            if user.strip():
                break
            else:
                print("username cant be blank")

        if user.lower() == 'exit':
            break
        message= ''.join(random.choices(string.ascii_letters, k=7))
        # message = input(user+"'s Message: ").strip()

        if not message:
                print("message can't be blank")
                continue


        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        try:
            f=producer.send('chat-messages', key=user,value={'user': user, 'message': message,'timestamp':timestamp})
            f.get(timeout=10)
            print("Message sent!")
            time.sleep(3)

        except Exception as e:
            print(f"failed to send message {e}")

    producer.close()


if __name__ == "__main__":
    create_kafka_topic("new_topic", num_partitions=2, replication_factor=1)
    producer()
