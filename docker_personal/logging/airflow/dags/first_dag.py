from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import psycopg2

# Database connection details
DB_CONN_DETAILS = {
    "dbname": "de_personal",
    "user": "postgres",
    "password": "animesh11",
    "host": "host.docker.internal",
    "port": "5432"
}

def fetch_road_data():
    """Fetches sample road data from PostgreSQL and prints it."""
    try:
        conn = psycopg2.connect(**DB_CONN_DETAILS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM roads_traffic.roads LIMIT 5;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)  # Airflow logs this
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error fetching data: {e}")

# Define DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 15),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "fetch_road_data",
    default_args=default_args,
    description="A simple DAG to fetch and log road data",
    schedule_interval=timedelta(hours=1),  # Runs every hour
    catchup=False,
)

# Task to fetch road data
fetch_data_task = PythonOperator(
    task_id="fetch_road_data",
    python_callable=fetch_road_data,
    dag=dag,
)

fetch_data_task  # Running single task

