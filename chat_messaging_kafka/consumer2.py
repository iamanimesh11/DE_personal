from kafka import KafkaConsumer, TopicPartition
import json
import psycopg2
from psycopg2 import sql

def consumer1():
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
        partition=1
        data = message.value
        user=data['user']
        msg_content=data['message']
        timestamp=data['timestamp']
        print(f"{user} : {msg_content}  {timestamp}")
        save_to_db(user,msg_content,timestamp, partition)


def save_to_db(user,message,timestamp,partition):
    try:
        connection =psycopg2.connect(
            dbname="airflow_ETL",
            user="airflow_user",
            password="animesh11",
            host="localhost",
            port="5432"
        )
        cursor=connection.cursor()

        insert_query=sql.SQL("""
        INSERT INTO "kafka_Schema".kafka_chat_message (username,message,timestamp,partition)
        VALUES (%s,%s,%s,%s)
        """)
        cursor.execute(insert_query,(user,message,timestamp,partition))
        connection.commit()
        print(f"{user}'s message stored in db")
    except Exception as e:
        print(f"error saving to database: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    consumer1()