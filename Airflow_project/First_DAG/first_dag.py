import os
from datetime import datetime
from airflow import DAG
import requests
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


# Function to send a message to Discord
def send_discord_notification(message):
    webhook_url = 'https://discord.com/api/webhooks/1293892426125021214/pJGAI1r9CKf6BzXyLj8_EqTzpEG1domttEXfYZ5qSIVpZu-sYN_QM3Rx3RxdViV7pmUo'  # Replace with your webhook URL
    data = {
        'content': message  # The message to send
    }
    requests.post(webhook_url, json=data)


# Example task function
def notify_task():
    send_discord_notification("Task has completed successfully!")

# Function to be called in the PythonOperator
def print_hello():
    file_path = "/home/animesh11/airflow/dags/Airflow_project/a.txt"

    try:
        # Check if file exists and count the lines
        with open(file_path, 'r') as fn:
            lines = fn.readlines()
            count = len(lines) + 1  # Increment by 1 for the next write
    except FileNotFoundError:
        # Start fresh if file doesn't exist
        count = 1

    # Write the next line with the count
    with open(file_path, 'a') as fn:
        fn.write(f'{count}: my name is unknown!\n')  # Append count and text
# Function to send a notification
# Function to send a notification via Termux

        
# Define the default_args dictionary
default_args = {
    'owner': 'user',
    'start_date': datetime(2024, 10, 11),  # Set the start date
    'retries': 1,
}
# Initialize the DAG
dag = DAG(
    'first_dag',
    default_args=default_args,
    # schedule_interval='*/1 * * * *',  # Run every 5 minutes
    schedule_interval=None,
    catchup=False,  # Prevent backfilling to avoid unnecessary runs
)

# Create tasks
start = EmptyOperator(task_id='start', dag=dag)

hello_task = PythonOperator(
    task_id='hello_task',
    python_callable=notify_task,
    dag=dag,
)

end = EmptyOperator(task_id='end', dag=dag)

# Set up dependencies
start >> hello_task >> end
# new iiiiiiffe