
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.task_group import TaskGroup
import hashlib

import logging
import requests

# Logger setup remains the same

default_args = {
    'owner': 'user',
    'start_date': datetime(2024, 10, 13),
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}
def extract_Data(url,**kwargs):
    try:
        response = requests.get(url, verify=False)
        return response.json()  # Make sure this data gets returned
    except requests.exceptions.RequestException as e:
        return None


def transform_data(**kwargs):
    # Pull data from extract_data task using XCom
    ti = kwargs['ti']
    task_ids = [f"quote_fetch.fetch_quote_{hashlib.md5(url.encode()).hexdigest()}"   for url in kwargs['urls']]
    data = ti.xcom_pull(task_ids='extract_data')  # Ensure 'extract_data' matches the task_id

    all_Data=[]

    for task_id in task_ids:
        data=ti.xcom_pull(task_ids=task_id)
        if data:
            all_Data.extend(data)

    if not all_Data:
        print("no return ")
        return []

    transformed_data = [(i['Author'], i['quote']) for i in all_Data]

    return transformed_data  # Optional if you'd like to pass it to another task


def load_data_into_db(**kwargs):
    ti=kwargs['ti']
    transform_data=ti.xcom_pull(task_ids='transform_data')
    logging.info(transform_task)
    if not transform_data:
        return

    #postgres connection
    postggrss_hook = PostgresHook(postgres_conn_id ='test_quoteInDATABASE')
    conn=postggrss_hook.get_conn()
    cursor=conn.cursor()

    insert_query = "INSERT INTO quotes (author, quote) VALUES (%s, %s)"
    cursor.executemany(insert_query, transform_data)
    conn.commit()
    cursor.close()
    conn.close()


# DAG definition
with DAG(
        'taskGroup__Quote_ETL_PIPE',
        default_args=default_args,
        schedule_interval=None,
        catchup=False,
) as dag:
    urls = [
        "https://quote-etl-api.vercel.app/quotes/?count=1",
        "https://quote-etl-api-2.vercel.app/quotes/?count=1"
    ]

    # Creating table using PostgresOperator
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='test_quoteInDATABASE',
        sql="""
           CREATE TABLE IF NOT EXISTS quotes (
               author VARCHAR(100),
               quote VARCHAR(100)
           );
           """,
    )

    with TaskGroup(group_id='quote_fetch') as task_Group:
        for url in urls:
            hash_url = hashlib.md5(url.encode()).hexdigest()
            sanitized_url = url.replace("https://", "").replace("/", "_").replace("?", "_").replace("&", "_").replace("=","_")

            task=PythonOperator(
                task_id=f"fetch_quote_{hash_url}",
                python_callable=extract_Data,
                op_kwargs={'url':url},
            )

    transform_task = PythonOperator(
        task_id='transform_data',  # Ensure task_id is correct
        python_callable=transform_data,
        provide_context=True,  # Context needed for pulling XCom data
        op_kwargs={'urls': urls},  # Pass the URLs for task_id generation

    )

    load_data_task = PythonOperator(
        task_id='load_data_task',  # Ensure task_id is correct
        python_callable=load_data_into_db,
        provide_context=True,  # Context needed for pulling XCom data
    )


    # Task flow
    create_table >> task_Group >> transform_task>> load_data_task


