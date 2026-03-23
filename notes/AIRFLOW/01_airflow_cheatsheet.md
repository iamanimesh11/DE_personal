# ⚡ Apache Airflow Cheatsheet — Quick Reference

> Syntax-first · Patterns · Copy-paste ready · Intermediate → DE level

---

## 📑 Table of Contents

| # | Topic |
|---|-------|
| 1 | [DAG Skeleton](#1-dag-skeleton) |
| 2 | [Core Operators — Quick Reference](#2-core-operators--quick-reference) |
| 3 | [Task Dependencies](#3-task-dependencies) |
| 4 | [Scheduling — Cron Quick Map](#4-scheduling--cron-quick-map) |
| 5 | [XCom — Pass Data Between Tasks](#5-xcom--pass-data-between-tasks) |
| 6 | [BranchPythonOperator](#6-branchpythonoperator) |
| 7 | [Sensors — Quick Reference](#7-sensors--quick-reference) |
| 8 | [Connections & Hooks](#8-connections--hooks) |
| 9 | [Error Handling & Retries](#9-error-handling--retries) |
| 10 | [TaskFlow API (Modern Style)](#10-taskflow-api-modern-style) |
| 11 | [Airflow CLI — Must Know Commands](#11-airflow-cli--must-know-commands) |
| 12 | [Variables & Environment](#12-variables--environment) |

---

## 1. DAG Skeleton

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# ── Default args applied to ALL tasks ──────────────────────────
default_args = {
    'owner'           : 'animesh',
    'retries'         : 3,
    'retry_delay'     : timedelta(minutes=5),
    'email_on_failure': True,
    'email'           : ['animesh@example.com'],
    'depends_on_past' : False,
}

# ── DAG definition ──────────────────────────────────────────────
with DAG(
    dag_id          = 'my_first_dag',
    default_args    = default_args,
    description     = 'A simple example DAG',
    schedule_interval = '@daily',          # or cron: '0 6 * * *'
    start_date      = datetime(2024, 1, 1),
    catchup         = False,               # don't backfill missed runs
    tags            = ['example', 'etl'],
) as dag:

    def say_hello():
        print("Hello from Airflow!")

    task1 = PythonOperator(
        task_id     = 'say_hello',
        python_callable = say_hello,
    )
```

---

## 2. Core Operators — Quick Reference

### PythonOperator
```python
from airflow.operators.python import PythonOperator

def extract_data(**kwargs):
    print("Extracting...")
    return {"rows": 1000}

extract = PythonOperator(
    task_id         = 'extract_data',
    python_callable = extract_data,
    op_kwargs       = {'source': 'mysql'},   # pass args to function
)
```

### BashOperator
```python
from airflow.operators.bash import BashOperator

run_script = BashOperator(
    task_id      = 'run_script',
    bash_command = 'python /opt/scripts/process.py --date {{ ds }}',
    #                                              ↑ Jinja template
)
```

### EmailOperator
```python
from airflow.operators.email import EmailOperator

send_report = EmailOperator(
    task_id = 'send_report',
    to      = 'team@example.com',
    subject = 'Pipeline Complete — {{ ds }}',
    html_content = '<h3>Pipeline ran successfully on {{ ds }}</h3>',
)
```

### DummyOperator / EmptyOperator
```python
from airflow.operators.empty import EmptyOperator  # Airflow 2.4+

start = EmptyOperator(task_id='start')
end   = EmptyOperator(task_id='end')
```

### SQLExecuteQueryOperator
```python
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

run_sql = SQLExecuteQueryOperator(
    task_id    = 'run_query',
    conn_id    = 'my_postgres',
    sql        = 'INSERT INTO summary SELECT * FROM raw WHERE date = {{ ds }};',
)
```

### SparkSubmitOperator
```python
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

spark_job = SparkSubmitOperator(
    task_id     = 'spark_transform',
    application = '/opt/spark/jobs/transform.py',
    conn_id     = 'spark_default',
    conf        = {'spark.executor.memory': '4g'},
)
```

### Operators Quick Map

| Operator | Does | Provider |
|----------|------|----------|
| `PythonOperator` | Run Python function | core |
| `BashOperator` | Run bash command | core |
| `EmptyOperator` | Placeholder / marker | core |
| `EmailOperator` | Send email | core |
| `SQLExecuteQueryOperator` | Run SQL | common.sql |
| `SparkSubmitOperator` | Submit Spark job | apache.spark |
| `S3ToRedshiftOperator` | Load S3 → Redshift | amazon |
| `GCSToBigQueryOperator` | Load GCS → BigQuery | google |
| `KubernetesPodOperator` | Run pod in K8s | cncf.kubernetes |
| `TriggerDagRunOperator` | Trigger another DAG | core |

---

## 3. Task Dependencies

```python
# ── Linear chain ─────────────────────────
extract >> transform >> load

# ── Multiple upstream ─────────────────────
[extract_a, extract_b] >> transform >> load

# ── Fan out ───────────────────────────────
extract >> [transform_sales, transform_users, transform_products]

# ── Diamond pattern ───────────────────────
start >> [task_a, task_b] >> join >> end

# ── set_upstream / set_downstream (old style) ─
transform.set_upstream(extract)
load.set_downstream(notify)

# ── Visual reference ─────────────────────
"""
extract_a ─┐
            ├──► transform ──► load ──► notify
extract_b ─┘
"""
```

---

## 4. Scheduling — Cron Quick Map

```
┌─────────── minute  (0-59)
│ ┌───────── hour    (0-23)
│ │ ┌─────── day of month (1-31)
│ │ │ ┌───── month   (1-12)
│ │ │ │ ┌─── day of week  (0-6, Sun=0)
│ │ │ │ │
* * * * *
```

| Schedule | Cron | Preset |
|----------|------|--------|
| Every minute | `* * * * *` | — |
| Every hour | `0 * * * *` | `@hourly` |
| Every day at midnight | `0 0 * * *` | `@daily` |
| Every day at 6 AM | `0 6 * * *` | — |
| Every Monday | `0 0 * * 1` | `@weekly` |
| 1st of every month | `0 0 1 * *` | `@monthly` |
| Every year Jan 1 | `0 0 1 1 *` | `@yearly` |
| Only once | — | `@once` |
| Never (manual only) | — | `None` |

```python
schedule_interval = '0 6 * * *'    # daily at 6 AM
schedule_interval = '@daily'        # midnight daily
schedule_interval = None            # manual trigger only
schedule_interval = timedelta(hours=6)  # every 6 hours
```

---

## 5. XCom — Pass Data Between Tasks

```
Task A ──► pushes value ──► XCom Store ──► Task B pulls value
```

```python
# ── Push XCom ────────────────────────────────────────────────
def push_data(**kwargs):
    kwargs['ti'].xcom_push(key='row_count', value=5000)
    # OR: just return a value — auto-pushed as 'return_value'
    return 5000

# ── Pull XCom ────────────────────────────────────────────────
def pull_data(**kwargs):
    ti = kwargs['ti']
    count = ti.xcom_pull(task_ids='push_data', key='row_count')
    print(f"Got {count} rows")

push_task = PythonOperator(task_id='push_data',  python_callable=push_data)
pull_task = PythonOperator(task_id='pull_data',  python_callable=pull_data)

push_task >> pull_task
```

> ⚠️ XCom is stored in the metadata DB — keep values **small** (IDs, counts, paths).
> Never push large DataFrames — use S3/GCS path instead.

---

## 6. BranchPythonOperator

```python
from airflow.operators.python import BranchPythonOperator

def choose_branch(**kwargs):
    day = kwargs['execution_date'].day_of_week
    if day == 0:          # Monday
        return 'full_load'
    return 'incremental_load'

branch = BranchPythonOperator(
    task_id         = 'branch_decision',
    python_callable = choose_branch,
)

full_load        = PythonOperator(task_id='full_load',        ...)
incremental_load = PythonOperator(task_id='incremental_load', ...)
notify           = EmptyOperator(task_id='notify',
                                 trigger_rule='none_failed_min_one_success')

branch >> [full_load, incremental_load] >> notify
```

```
          ┌──► full_load ────────┐
branch ───┤                      ├──► notify
          └──► incremental_load ─┘
```

---

## 7. Sensors — Quick Reference

> Sensors **wait** for a condition to be true before proceeding.

```python
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.python    import PythonSensor
from airflow.providers.http.sensors.http import HttpSensor

# Wait for file to appear
wait_for_file = FileSensor(
    task_id         = 'wait_for_file',
    filepath        = '/data/input/orders_{{ ds }}.csv',
    poke_interval   = 60,    # check every 60 seconds
    timeout         = 3600,  # fail after 1 hour
    mode            = 'poke',  # 'reschedule' for long waits
)

# Wait for HTTP endpoint to return 200
wait_for_api = HttpSensor(
    task_id      = 'wait_for_api',
    http_conn_id = 'my_api',
    endpoint     = '/health',
    poke_interval = 30,
    timeout       = 600,
)
```

| Mode | Behaviour | Use when |
|------|-----------|----------|
| `poke` | Holds a worker slot while waiting | Short waits (< 5 min) |
| `reschedule` | Releases worker slot between checks | Long waits (hours) ✅ |

---

## 8. Connections & Hooks

```python
# ── Define connection in UI or CLI ───────────────────────────
# Conn ID: my_postgres
# Type: Postgres
# Host: localhost  Port: 5432  Schema: mydb

# ── Use connection via Hook ───────────────────────────────────
from airflow.providers.postgres.hooks.postgres import PostgresHook

def query_postgres():
    hook = PostgresHook(postgres_conn_id='my_postgres')
    df   = hook.get_pandas_df("SELECT * FROM orders LIMIT 100")
    print(df.head())

# ── S3 Hook ───────────────────────────────────────────────────
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def upload_to_s3():
    hook = S3Hook(aws_conn_id='my_aws')
    hook.load_file(
        filename    = '/tmp/output.csv',
        key         = 'data/output.csv',
        bucket_name = 'my-bucket',
        replace     = True,
    )
```

---

## 9. Error Handling & Retries

```python
default_args = {
    'retries'             : 3,
    'retry_delay'         : timedelta(minutes=5),
    'retry_exponential_backoff': True,   # 5min, 10min, 20min...
    'email_on_failure'    : True,
    'email_on_retry'      : False,
    'on_failure_callback' : my_alert_function,
}

# ── Per-task override ─────────────────────────────────────────
risky_task = PythonOperator(
    task_id         = 'risky_task',
    python_callable = risky_function,
    retries         = 5,
    retry_delay     = timedelta(seconds=30),
    execution_timeout = timedelta(minutes=10),  # kill if runs too long
)

# ── On failure callback ───────────────────────────────────────
def alert_slack(context):
    dag_id  = context['dag'].dag_id
    task_id = context['task_instance'].task_id
    print(f"FAILED: {dag_id}.{task_id}")
    # send Slack/PagerDuty alert here
```

---

## 10. TaskFlow API (Modern Style)

> **Airflow 2.0+ — cleaner Python, no boilerplate.**

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(schedule_interval='@daily', start_date=datetime(2024,1,1), catchup=False)
def my_etl_pipeline():

    @task
    def extract():
        return {"data": [1, 2, 3], "count": 3}

    @task
    def transform(raw: dict):
        return [x * 2 for x in raw["data"]]

    @task
    def load(processed: list):
        print(f"Loading {len(processed)} records")

    # Dependencies inferred from function calls ✨
    raw     = extract()
    cleaned = transform(raw)
    load(cleaned)

dag_instance = my_etl_pipeline()
```

---

## 11. Airflow CLI — Must Know Commands

```bash
# ── DAG operations ────────────────────────────────────────────
airflow dags list                          # list all DAGs
airflow dags trigger my_dag               # manual trigger
airflow dags pause   my_dag               # pause DAG
airflow dags unpause my_dag               # unpause DAG
airflow dags backfill my_dag \
  --start-date 2024-01-01 \
  --end-date   2024-01-31               # backfill missed runs

# ── Task operations ───────────────────────────────────────────
airflow tasks list  my_dag               # list tasks in DAG
airflow tasks test  my_dag task_id 2024-01-01  # test single task
airflow tasks clear my_dag --start-date 2024-01-01  # rerun tasks

# ── DB ────────────────────────────────────────────────────────
airflow db init                           # initialize metadata DB
airflow db upgrade                        # upgrade schema
airflow db check                          # check DB connection

# ── Users ─────────────────────────────────────────────────────
airflow users create \
  --username admin --password admin \
  --role Admin --email admin@example.com \
  --firstname A --lastname B

# ── Variables & Connections ───────────────────────────────────
airflow variables set my_key my_value
airflow variables get my_key
airflow connections add my_conn \
  --conn-type postgres --conn-host localhost
```

---

## 12. Variables & Environment

```python
from airflow.models import Variable

# ── Get variable (set in UI or CLI) ──────────────────────────
env        = Variable.get('environment')                    # string
config     = Variable.get('pipeline_config', deserialize_json=True)  # dict
secret_key = Variable.get('api_key', default_var='fallback')

# ── Use in templates (Jinja) ──────────────────────────────────
BashOperator(
    task_id      = 'use_var',
    bash_command = 'echo {{ var.value.environment }}',
)

# ── Jinja built-in template variables ─────────────────────────
"""
{{ ds }}              → execution date as 'YYYY-MM-DD'
{{ ds_nodash }}       → execution date as 'YYYYMMDD'
{{ ts }}              → execution timestamp ISO format
{{ dag.dag_id }}      → current DAG id
{{ task.task_id }}    → current task id
{{ run_id }}          → unique run identifier
{{ prev_ds }}         → previous execution date
{{ next_ds }}         → next execution date
"""
```

---

*⚡ Airflow Cheatsheet · Syntax-first · Copy-paste ready*
