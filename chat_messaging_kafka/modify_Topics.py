from kafka.admin import KafkaAdminClient,NewTopic
from kafka.errors import TopicAlreadyExistsError

def create_kafka_topic(admin_client,topic_name,num_partitions,replication_factor):
    try:
        #initialize kafkaclient
        topic=NewTopic (
            name=topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor
        )
        admin_client.create_topics(new_topics=[topic],validate_only=False)
        print(f"topic '{topic_name}' created successfully")

    except TopicAlreadyExistsError:
        print(f"topic '{topic_name} already exist !")

    except Exception as e:
        print(f"error creating topic :{e}")

def delete_kafka_topic(admin_client,topic_name):
    try:
        admin_client.delete_topics(topics=[topic_name])
        print(f"topic {topic_name} deleted successfully! " )
    except Exception as e:
        print(f"Error deleting topic: {e}")

def describe_kafka_topic(admin_client,topic_name):
    try:
        topics_metadata = admin_client.describe_topics(topics=[topic_name])
        for topic in topics_metadata:
            print(f"Topic: {topic}")
    except Exception as e:
        print(f"Error describing topic: {e}")

def alter_kafka_topic(admin_client,topic_name,num_partitions):
    try:

        partition_assignments = [NewPartitions(i) for i in range(num_partitions)]
        admin_client.create_partitions(
            topic_partitions={topic_name:num_partitions},
            validate_only=False
        )
        print(f"topic  {topic_name} altered to {num_partitions} partitions successfully")

    except Exception as e:
        print(f"error altering topic: {e}")


def list_all_topics(admin_client):
    try:
        topics=admin_client.list_topics()
        print("Avaialble topics: ")
        for topic in topics:
            print(f" - {topic}")

    except Exception as e:
        print("Error listing topics")

def main():
    try:
        admin_client=KafkaAdminClient(
            bootstrap_servers='172.19.165.234:9092',
            client_id="kafka_topic_manager"
        )
        while True:
            print("\nKafka Topic Manager")
            print("1. Create Topic")
            print("2. Delete Topic")
            print("3. Alter Topic (Add Partitions)")
            print("4. Describe Topic")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                topic_name = input("Enter topic name: ")
                num_partitions = int(input("Enter number of partitions: "))
                replication_factor = int(input("Enter replication factor: "))
                create_kafka_topic(admin_client, topic_name, num_partitions, replication_factor)
            elif choice == "2":
                topic_name = input("Enter topic name to delete: ")
                delete_kafka_topic(admin_client, topic_name)
            elif choice == "3":
                topic_name = input("Enter topic name to alter: ")
                num_partitions = int(input("Enter new number of partitions: "))
                alter_kafka_topic(admin_client, topic_name, num_partitions)
            elif choice == "4":
                topic_name = input("Enter topic name to describe: ")
                describe_kafka_topic(admin_client, topic_name)

            elif choice == "5":

                list_all_topics(admin_client)

            elif choice == "6":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
         print(f"Error: {e}")

    finally:
         admin_client.close()


if __name__ == "__main__":
   main()
