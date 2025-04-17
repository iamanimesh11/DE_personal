from airflow import  DAG
from airflow.operators.python import  PythonOperator
from datetime import datetime,timedelta
import requests
import psycopg2
import logging
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import  TaskGroup
from airflow.hooks.postgres_hook import PostgresHook
import time


etl_logger = logging.getLogger('ETLLogger')
etl_logger.setLevel(logging.INFO)

file_handler =logging.FileHandler('etl_log.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

etl_logger.addHandler(file_handler)

def log_task_status(task_id,start_time,status,record_fetched,error_message=None):
    postgres_hook =PostgresHook(postgres_conn_id ='QuoteInDatabase_ETL')
    conn = postgres_hook.get_conn()
    cursor =conn.cursor()

    run_time =datetime.now()
    duration =timedelta(seconds=time.time()-start_time)
    insert_log_query=""" INSERT INTO TaskLogs (task_id,run_time,duration,status,records_fetched,error_message)
    VALUES (%s,%s,%s,%s,%s,%s);
    """

    cursor.execute(insert_log_query,(task_id,run_time,duration,status,record_fetched,error_message))
    conn.commit()
    cursor.close()
    conn.close


def extract_data(**kwargs):
    start_time =time.time()
    try:
        data=[]
        for i in range(50):
            url = "https://lucifier-quotes.vercel.ap/api/quotes"
            response=requests.get(url,verify=False)
            etl_logger.info(response.json())
            data.append(response.json()[0])
        etl_logger.info(f"{len(data)} Data extraction successfully")
        log_task_status('extract_Data',start_time,'success',len(data))

        return data

    except requests.exceptions.RequestException as e:
        etl_logger.error(f"Error feching data : {e}")
        load_Data_task('extract_Data',start_time,'fail',error_message =str(e))


        return None

def transform_data(**kwargs):
    start_time=time.time()
    ti=kwargs['ti']
    data =ti.xcom_pull(task_ids='extract_Data')
    if len(data)==0:
        etl_logger.error("no data to transform")
        log_task_status('transfomr_Data',start_time,'No data to transform',len(data))

        return []
    transformed_Data =[]

    for i in data:
        transformed_Data.append((i['author'],i['quote']))
    etl_logger.info(f"total records transformed : {len(transformed_Data)}")
    print(transformed_Data)
    log_task_status('transofmr_Data',start_time,'success',len(data))

    return transformed_Data


def load_Data_into_Db(**kwargs):
    start_time=time.time()

    ti=kwargs['ti']
    transfomr_Data =ti.xcom_pull(task_ids='transform_Data')
    etl_logger.info (f"Data to transfomr :{transfomr_Data}")

    if not transform_data:
        log_task_status('load_Data',start_time,'No data to load',len(transfomr_Data))
        etl_logger.error("no data")

        return
#postgres connection

    Postgres_hook =PostgresHook(postgres_conn_id ='quoteinDATABASE_ETL')
    conn =Postgres_hook.get_conn()
    cursor=conn.cursor()

    insert_Query = "INSERT INTO Quotes (Author,Quote) VALUES (%s,%s)"
    print(insert_Query)
    cursor.executemany(insert_Query,transform_data)
    conn.commit()
    cursor.close()
    conn.close()
    log_task_status('load_data',start_time,"successs",len(transfomr_Data))




default_Args = {
    'owner': 'user',
    'stat_date': datetime(2024, 10, 22),
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
    'depends_on_past': False,
}

with DAG(
        'test',
        default_args=default_Args,
        schedule_interval=None,
        catchup=False,

) as DAG:
    extract_task = PythonOperator(
        task_id='extract_Data',
        python_callable=extract_data,
        provide_context=True,
        retries=0,
        retry_delay=timedelta(minutes=1),
    )
    transform_task = PythonOperator(
        task_id ='transform_task',
        python_Callable=transform_Data,
        provide_context=True,
        retries=0,
        retry_delay=timedelta(minutes=1)
    )

    load_Data_task = PythonOperator(
        task_id='load_Data_task',
        python_callable=load_data_Task,
        provide_context=True,
        retries=0,
        retry_delay=timedelta(minutes=1)
    )
    create_TabLE =PostgresOperator(
        task_id ='create_Table',
        postgres_conn_id ='t',
        sql ="""
        CREATE TABLE IF NOT EXISTS Quotes (
        Author varchar(100),
        Quote text 
        );
        
        CREATE TABLE IF NOT EXISTS TaskLogs (
        id SERIAL PRIMARY KEY,
        task_id VARCHAR(255).
        run_time TIMESTAMP,
        duration INTERVAL,
        status VARCHAR(50),
        records_fetched INT,
        error_message TEXT
        );        
         """
    )

    create_TabLE >>extract_task>>transform_task>>load_Data_task

