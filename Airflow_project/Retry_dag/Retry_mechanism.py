from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowFailException
import requests

# Function to simulate failure in the first 2 tries
def my_task(**kwargs):
    # Get the current retry number from context
    retry_number = kwargs['ti'].try_number
    if retry_number < 3:
        # Simulate failure for the first two tries
        raise Exception(f"Intentional failure on try number: {retry_number}")
    else:
        # Success on the 3rd try
        print(f"Success on try number: {retry_number}")
        with open('/home/animesh11/airflow/dags/Airflow_project/Retry_dag/retry_log.txt', 'a') as f:
            f.write(f"Task succeeded on try number: {retry_number}\n")

# Define default_args
default_args = {
    'owner': 'user',
    'start_date': datetime(2024, 10, 10),
    'retries': 1,  # Allow 3 retries
    'retry_delay': timedelta(seconds=10),  # Delay between retries
}

# Initialize DAG
dag = DAG(
    'retry_task_dag',
    default_args=default_args,
    schedule_interval=None,  # Set to None for manual trigger
    catchup=False,
)

# Create PythonOperator task
task = PythonOperator(
    task_id='retry_task',
    python_callable=my_task,
    provide_context=True,  # Enable context passing
    dag=dag,
)

# Set up the DAG task dependencies
