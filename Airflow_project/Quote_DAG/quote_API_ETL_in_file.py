from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import psycopg2
import logging


# Create a logger for your ETL process
etl_logger = logging.getLogger('ETLLogger')
etl_logger.setLevel(logging.INFO)

# Create file handler to log to the specified file
file_handler = logging.FileHandler('/home/animesh11/airflow/dags/Airflow_project/etl_log.log')
file_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
etl_logger.addHandler(file_handler)

def send_discord_notification(msg):
    webhook_url = "https://discord.com/api/webhooks/1293892426125021214/pJGAI1r9CKf6BzXyLj8_EqTzpEG1domttEXfYZ5qSIVpZu-sYN_QM3Rx3RxdViV7pmUo"
    message = {"content": msg}
    requests.post(webhook_url, json=message)
def extract_Data(**kwargs):
    try:
        url = "https://lucifer-quotes.vercel.app/api/quotes"
        response = requests.get(url, verify=False)
        etl_logger.info("Data extraction successfull")

        return response.json()
    except requests.exceptions.RequestException as e:
        etl_logger.error(f"Error fetching data: {e}")
        return None

def transform_data(data):
    if data is None:
        etl_logger.error("no  data to transform")
        return []
    transformed_Data =[]
    count =0
    messages=[]
    for i in data:
        author = i['author']
        quote = i['quote']
        message = f"{author}: {quote}"
        transformed_Data.append(message + "\n")
        etl_logger.info(f"Transformed data: {author} - {quote}")
        messages.append(message)  # Store individual quotes in the list
        count+=1
    final_message = "\n".join(messages) + f"\n\nTotal quotes processed: {count}"
    etl_logger.info(f"Total records transformed: {len(transformed_Data)}")

    send_discord_notification("*******************")
    send_discord_notification(final_message)
    return transformed_Data
def load_data(data):
    if not data:
        etl_logger.error("No data to load")
        return
    with open("/home/animesh11/airflow/dags/Airflow_project/JSON_dATA.txt", "a") as f:
        f.writelines(data)
    etl_logger.info(f"Data successfully loaded: {len(data)} records.")



def run_etl(**kwargs):
    etl_logger.info("Starting ETL process.")
    try:
         data =extract_Data()
         transformed_data = transform_data(data)
         load_data(transformed_data)
         etl_logger.info("ETL process completed.")

    except Exception as e:
        etl_logger.info(f"ETL JOB FAILED : {e}")
        send_discord_notification(f"ETL JOB FAILED : {e}")
        raise

# Define default_args
default_args = {
    'owner': 'user',
    'start_date': datetime(2024, 10, 13),
    'retries': 1,  # Allow 3 retries
    'retry_delay': timedelta(seconds=10),  # Delay between retries
}

# Initialize DAG
dag = DAG(
    'Quote_ETL_PIPE_IN_FILE',
    default_args=default_args,
    schedule_interval=None,  # Run every 1 minutes
    # schedule_interval='*/1 * * * *',  # Run every 1 minutes
    catchup=False,
)
# Create PythonOperator task
task = PythonOperator(
    task_id='QUOTE_fetch_task',
    python_callable=run_etl,
    provide_context=True,  # Enable context passing
    dag=dag,
)





