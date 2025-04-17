from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta
import requests
import psycopg2
import logging
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup
from airflow.hooks.postgres_hook import PostgresHook
import time

etl_logger =logging.getLogger('ETLlogger')
etl_logger.setLevel(logging.INFO)

FORMATTER =logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')


def extract_Data(**kwargs):
    start_time=time.time()
    try:
        url = "https://quote-etl-api-2.vercel.app/quotes/?count=100"
        response = requests.get(url,verify=False)
        etl_logger.info(f" extracted data length : {len(response.json())}")
        return response.json()

    except requests.exceptions.RequestException as e:
        etl_logger.error(f"error fetching data : {e}")

        return None


def transform_data (**kwargs):
    start_Time=time.time()
    ti=kwargs['ti']
    data =ti.xcom_pull(task_ids='extract_task')
    if len(data) ==0:
        etl_logger.error(f"No data to transform ,count : {len(data)}")
        return []
    transformed_Data =[]
    for i in data:
        x=(i['name'],i['brand'],i['processor name'],i['RAM'],i['SSD'],i['display'],i['price'],i['product review_y'],i['ratings'])
        transformed_Data.append(x)

    etl_logger.info(f" Total records transformed: {len(transformed_Data)}")
    return transformed_Data

def load_Data_into_Db(**kwargs):
    start_time=time.time()
    ti=kwargs['ti']
    transform_data = ti.xcom_pull(task_ids="transform_Data")
    etl_logger.info(f" data to transform : {transform_data}")

    if not transform_data:
        etl_logger.error("no data to load")

        return

    postgres_hook =PostgresHook(postgres_conn_id ="QuoteInDatabase_ETL")
    conn =postgres_hook.get_conn()
    cursor =conn.cursor()

    insert_query= "INSERT INTO flipkart_LAPTOPS (name,brand,processor_name,RAM,SSD,display,price,product_review_y,ratings) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.executemany(insert_query,transform_data)
    conn.commit()
    cursor.close()
    conn.close()
    etl_logger.info(f" successfully loaded {len(transform_data)} records into database")


default_Args = {
    'owner':'user',
    'start_date':datetime(2024,10,24),
    'retries':1,
    'retry_delay':timedelta(seconds=10),
    'depends_on_past':False,

}

with DAG (
    'FLipkart_laptop_ETL',
    default_args=default_Args,
    schedule_interval=None,
    catchup=False
) as dag:
    extract_Task=PythonOperator(
        task_id="extract_task",
        python_callable=extract_Data,
        provide_context=True,
        retries=0,
        retry_delay=timedelta(minutes=1),

    )

    transform_data=PythonOperator(
        task_id="transform_Data",
        python_callable=transform_data,
        provide_context=True,
        retries=0,
        retry_delay=timedelta(minutes=1),
    )
    load_Data_task=PythonOperator(
        task_id='load_Data',
        python_callable=load_Data_into_Db,
        provide_context=True,
        retries=0,
        retry_delay=timedelta(minutes=1),
    )
    create_table=PostgresOperator(
        task_id='Create_table',
        postgres_conn_id='QuoteInDatabase_ETL',
        sql="""
        CREATE TABLE IF NOT EXISTS public.flipkart_LAPTOPS (
        name TEXT,
        brand VARCHAR(100),
        processor_name TEXT,
        RAM TEXT,
        SSD TEXT,
        display TEXT,
        price INT,
        product_review_y TEXT,
        ratings DECIMAL(3,2)
        )
        """
    )
    create_table >> extract_Task >> transform_data >> load_Data_task
