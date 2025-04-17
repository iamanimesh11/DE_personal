
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import psycopg2
import logging
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup
from airflow.hooks.postgres_hook import PostgresHook
import time

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
    start_time=time.time()
    try:
        i=0
        data=[]
        while i<0:
            url = "https://lucifer-quotes.vercel.app/api/quotes"
            response = requests.get(url, verify=False)
            etl_logger.info(response.json())
            data.append(response.json()[0])
            i+=1

        etl_logger.info(f"{len(data)} Data extraction successfully")
        log_task_status('extract_data', start_time,'success', len(data))

        return data
    except requests.exceptions.RequestException as e:
        etl_logger.error(f"Error fetching data: {e}")
        log_task_status('extract_data', start_time,'fail', error_message=str(e))

        return None
def transform_data(**kwargs):
    start_time=time.time()
    ti=kwargs['ti']
    data=ti.xcom_pull(task_ids='extract_data')
    if len(data) ==0:
        etl_logger.error("no  data to transform")
        log_task_status('transform_data', start_time,'NO_data_received', len(data))

        return []
    transformed_Data =[]

    for i in data:
        transformed_Data.append((i['author'],i['quote']))
    etl_logger.info(f"Total records transformed: {len(transformed_Data)}")
    print(transformed_Data)
    # send_discord_notification("*******************")
    log_task_status('transform_data', start_time, 'success',len(data))

    return transformed_Data
def load_data_into_db(**kwargs):
    start_time=time.time()

    ti=kwargs['ti']
    transform_data=ti.xcom_pull(task_ids='transform_data')
    etl_logger.info(f"Data To transform : {transform_data}")

    if not transform_data:
        log_task_status('load_data', start_time, 'No data to load',len(transform_data))
        etl_logger.error("No data to load")


        return

    #postgres connection
    postggrss_hook = PostgresHook(postgres_conn_id ='QuoteInDatabase_ETL')
    conn=postggrss_hook.get_conn()
    cursor=conn.cursor()

    insert_query = "INSERT INTO Quotes (Author, Quote) VALUES (%s, %s)"
    print(transform_data)
    cursor.executemany(insert_query, transform_data)
    conn.commit()
    cursor.close()
    conn.close()
    log_task_status('load_data', start_time, 'success_loaded_into_DB', len(transform_data))

    etl_logger.info(f"Successfully loaded {len(transform_data)} records into the database.")


def log_task_status(task_id,start_time,status,record_fetched,error_message=None):
    postgres_hook= PostgresHook(postgres_conn_id='QuoteInDatabase_ETL')
    conn=postgres_hook.get_conn()
    cursor=conn.cursor()

    run_time=datetime.now()
    duration=timedelta(seconds=time.time()-start_time)
    insert_log_query =""" INSERT INTO TaskLogs (task_id,run_time,duration,status,records_fetched,error_messsage) 
    VALUES (%s, %s, %s ,%s ,%s ,%s );
    """

    cursor.execute(insert_log_query,(task_id,run_time,duration,status,record_fetched,error_message))
    conn.commit()
    cursor.close()
    conn.close

# Define default_args
default_args = {
    'owner': 'user',
    'start_date': datetime(2024, 10, 13),
    'retries': 1,  # Allow 3 retries
    'retry_delay': timedelta(seconds=10),  # Delay between retries
    'depends_on_past' : False,
}

# Initialize DAG
with DAG(
    'Quote_ETL_PIPE_in_Database',
    default_args=default_args,
    # schedule_interval='*/1 * * * *',  # Run every 1 minutes
    schedule_interval=None,  # Run every 1 minutes

        catchup=False,
) as dag:
    # Create PythonOperator task
    extract_Task=PythonOperator(
        task_id="extract_data",
        python_callable=extract_Data,
        provide_context=True,
        retries=0,
        retry_delay=timedelta(minutes=1),
    )
    transform_task=PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        provide_context=True,
        retries=0,
        retry_delay=timedelta(minutes=1),
    )
    # Task to load data into PostgreSQL
    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data_into_db,
        provide_context=True,
        retries=0,
        retry_delay=timedelta(minutes=1),
    )
    create_table= PostgresOperator(
        task_id ='create_table',
        postgres_conn_id='QuoteInDatabase_ETL',
        sql="""
        CREATE TABLE IF NOT EXISTs Quotes (
        Author varchar(100),
        Quote Text
        );
        
        CREATE TABLE IF NOT EXISTS TaskLogs (
            id SERIAL PRIMARY KEY,
            task_id VARCHAR(255),
            run_time TIMESTAMP,
            duration INTERVAL,
            status VARCHAR(50),
            records_fetched INT,
            error_message TEXT
        );

        """ ,
    )
    # dvtt

    create_table >> extract_Task >> transform_task >> load_data_task

