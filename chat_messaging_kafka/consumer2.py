from kafka import KafkaConsumer, TopicPartition
import json
import psycopg2
from psycopg2 import sql

def consumer1():
    consumer = KafkaConsumer(
        'chat-messages',  # Kafka topic

        group_id='chat-consumer-group',  # Consumer group ID

        bootstrap_servers='172.19.165.234:9092',  # Replace with your Kafka server
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        enable_auto_commit=False , # Disable auto commit to handle offsets manually
    )


    print("Chat Consumer started. Listening for messages on Partition 0:")

    for message in consumer:
        partition = message.partition
        data = message.value
        user=data['user']
        msg_content=data['message']
        timestamp=data['timestamp']

        print(f"{user} : {msg_content}  {timestamp}")
        save_to_db(user,msg_content,timestamp, partition)
        consumer.commit()


def save_to_db(user,message,timestamp,partition):
    try:
        table_name="kafka_chat_message"
        connection =psycopg2.connect(
            dbname="airflow_ETL",
            user="airflow_user",
            password="animesh11",
            host="localhost",
            port="5432"
        )
        cursor=connection.cursor()

        insert_query=sql.SQL("""
        INSERT INTO "kafka_Schema".{table} (username,message,timestamp,partition)
        VALUES (%s,%s,%s,%s)
        """).format(table=sql.Identifier(table_name))  # Use sql.Identifier for dynamic table name

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