# ⚙️ Apache Airflow — Advanced & Data Engineering Patterns

> Production patterns · Dynamic DAGs · Testing · Best practices · DE-specific

---

## 📑 Table of Contents

| # | Topic |
|---|-------|
| 1 | [Dynamic DAGs](#1-dynamic-dags) |
| 2 | [DAG Factory Pattern](#2-dag-factory-pattern) |
| 3 | [Callbacks — Full Reference](#3-callbacks--full-reference) |
| 4 | [Data-Aware Scheduling (Datasets)](#4-data-aware-scheduling-datasets) |
| 5 | [Deferrable Operators](#5-deferrable-operators) |
| 6 | [Custom Operators](#6-custom-operators) |
| 7 | [Custom Hooks](#7-custom-hooks) |
| 8 | [Testing DAGs](#8-testing-dags) |
| 9 | [Airflow + dbt Integration](#9-airflow--dbt-integration) |
| 10 | [Airflow + Spark Integration](#10-airflow--spark-integration) |
| 11 | [Airflow on AWS (MWAA)](#11-airflow-on-aws-mwaa) |
| 12 | [Production Best Practices](#12-production-best-practices) |
| 13 | [Common Pitfalls & Fixes](#13-common-pitfalls--fixes) |
| 14 | [Performance Tuning](#14-performance-tuning) |
| 15 | [Advanced DE Interview Q&A](#15-advanced-de-interview-qa-) |

---

## 1. Dynamic DAGs

> **Generate multiple DAGs or tasks programmatically from config/data.**
> Avoids copy-pasting DAG files for every table/source/client.

### Dynamic Tasks from a list

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Config-driven — add a table, get a new task automatically
TABLES = ['orders', 'customers', 'products', 'payments']

def process_table(table_name: str):
    print(f"Processing table: {table_name}")

with DAG(
    dag_id          = 'dynamic_table_pipeline',
    schedule_interval = '@daily',
    start_date      = datetime(2024, 1, 1),
    catchup         = False,
) as dag:

    from airflow.operators.empty import EmptyOperator

    start = EmptyOperator(task_id='start')
    end   = EmptyOperator(task_id='end')

    for table in TABLES:
        task = PythonOperator(
            task_id         = f'process_{table}',
            python_callable = process_table,
            op_kwargs       = {'table_name': table},
        )
        start >> task >> end

# Result:
# start ──► process_orders ────┐
#       ──► process_customers ─┤
#       ──► process_products ──┼──► end
#       ──► process_payments ──┘
```

---

### Dynamic Tasks from DB/config file

```python
import json, os

# Load config from JSON file (or DB query)
config_path = os.path.join(os.path.dirname(__file__), 'pipeline_config.json')
with open(config_path) as f:
    pipeline_config = json.load(f)

# pipeline_config.json:
# {
#   "pipelines": [
#     {"name": "orders",    "source": "mysql",   "target": "redshift"},
#     {"name": "customers", "source": "postgres", "target": "redshift"}
#   ]
# }

with DAG('config_driven_dag', schedule_interval='@daily',
         start_date=datetime(2024,1,1), catchup=False) as dag:

    for pipeline in pipeline_config['pipelines']:
        PythonOperator(
            task_id         = f"load_{pipeline['name']}",
            python_callable = run_pipeline,
            op_kwargs       = pipeline,
        )
```

> ⚠️ **Important:** Don't query a DB or make HTTP calls at DAG parsing time.
> Airflow parses DAG files every 30 seconds — expensive calls will slow down the scheduler.
> Use config files or environment variables instead.

---

## 2. DAG Factory Pattern

> **One function generates multiple complete DAGs — DRY at the DAG level.**

```python
# dag_factory.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def create_etl_dag(
    dag_id: str,
    source_table: str,
    target_table: str,
    schedule: str,
) -> DAG:

    def extract(**kwargs):
        print(f"Extracting from {source_table}")
        return {"rows": 1000, "source": source_table}

    def transform(**kwargs):
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids='extract')
        print(f"Transforming {data['rows']} rows")

    def load(**kwargs):
        print(f"Loading into {target_table}")

    with DAG(
        dag_id            = dag_id,
        schedule_interval = schedule,
        start_date        = datetime(2024, 1, 1),
        catchup           = False,
        tags              = ['factory', source_table],
    ) as dag:

        t_extract   = PythonOperator(task_id='extract',   python_callable=extract)
        t_transform = PythonOperator(task_id='transform', python_callable=transform)
        t_load      = PythonOperator(task_id='load',      python_callable=load)

        t_extract >> t_transform >> t_load

    return dag


# ── Generate DAGs ─────────────────────────────────────────────
# Each appears as a separate DAG in the Airflow UI

orders_dag   = create_etl_dag('etl_orders',   'raw_orders',   'fct_orders',   '@daily')
customers_dag= create_etl_dag('etl_customers','raw_customers','dim_customers','@weekly')
products_dag = create_etl_dag('etl_products', 'raw_products', 'dim_products', '@daily')
```

---

## 3. Callbacks — Full Reference

> **4 types of callbacks — for alerting, monitoring, and cleanup.**

```python
def on_success_callback(context):
    dag_id  = context['dag'].dag_id
    run_id  = context['run_id']
    print(f"✅ DAG {dag_id} succeeded — run {run_id}")

def on_failure_callback(context):
    task_instance = context['task_instance']
    exception     = context.get('exception')
    # Send Slack/PagerDuty alert
    send_slack_alert(
        f"❌ Task {task_instance.task_id} failed\n"
        f"DAG: {task_instance.dag_id}\n"
        f"Error: {exception}"
    )

def on_retry_callback(context):
    ti = context['task_instance']
    print(f"🔄 Retrying {ti.task_id} — attempt {ti.try_number}")

def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    print(f"⏰ SLA missed for tasks: {task_list}")

with DAG(
    dag_id               = 'production_dag',
    on_success_callback  = on_success_callback,   # DAG level
    on_failure_callback  = on_failure_callback,   # DAG level
    sla_miss_callback    = sla_miss_callback,
    default_args = {
        'on_failure_callback': on_failure_callback,  # task level
        'on_retry_callback'  : on_retry_callback,    # task level
        'sla'                : timedelta(hours=1),   # task SLA
    },
    ...
) as dag:
    ...
```

### Callback Context Keys

```python
# Available in context dict:
context['dag']              # DAG object
context['dag_run']          # DagRun object
context['task']             # Task object
context['task_instance']    # TaskInstance (ti) object
context['execution_date']   # logical date
context['ds']               # execution date string
context['run_id']           # unique run id
context['exception']        # exception (on_failure only)
context['reason']           # failure reason string
```

---

## 4. Data-Aware Scheduling (Datasets)

> **Airflow 2.4+ — trigger DAGs based on data being produced, not just time.**

```python
from airflow import Dataset

# Define datasets (logical pointers to data)
orders_dataset   = Dataset('s3://my-bucket/orders/')
customers_dataset= Dataset('s3://my-bucket/customers/')

# ── Producer DAG — marks dataset as updated on success ────────
with DAG('producer_dag', schedule_interval='@daily', ...) as dag:

    load_orders = PythonOperator(
        task_id         = 'load_orders',
        python_callable = load_fn,
        outlets         = [orders_dataset],  # ← marks dataset updated
    )

# ── Consumer DAG — runs when dataset is updated ───────────────
with DAG(
    'consumer_dag',
    schedule = [orders_dataset, customers_dataset],  # ← wait for both
    ...
) as dag:

    run_report = PythonOperator(
        task_id         = 'run_report',
        python_callable = report_fn,
    )
```

```
Producer DAG runs → orders/ updated → Consumer DAG auto-triggered
                                       (no cron needed!)
```

> **Q: Why use Datasets over cron scheduling?**
> Datasets create **event-driven pipelines** — consumer runs only when
> upstream data is actually ready, not just because the clock ticked.
> Prevents empty runs when upstream is delayed.

---

## 5. Deferrable Operators

> **Airflow 2.2+ — tasks that wait without holding a worker slot.**

```
Normal Sensor:                    Deferrable Operator:
Worker slot occupied ████████     Worker slot released ░░░░░░░░
while waiting (wasteful)          while waiting (efficient) ✅
```

```python
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator

# deferrable=True → releases worker while job runs in Glue
run_glue = GlueJobOperator(
    task_id     = 'run_glue_job',
    job_name    = 'my-glue-job',
    deferrable  = True,          # ← key flag
    aws_conn_id = 'my_aws',
)
```

> **Q: When to use deferrable operators?**
> For long-running external jobs (30 min Spark jobs, Glue crawlers, BigQuery queries).
> They free up worker slots while waiting — saves infra cost at scale.

> **Q: What is a Triggerer in Airflow?**
> A new Airflow component (2.2+) that manages deferred tasks using async I/O.
> Must be running alongside the Scheduler for deferrable operators to work.

---

## 6. Custom Operators

> **When no existing operator fits — build your own.**

```python
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """
    Custom operator to run data quality checks on a table.
    """

    # Define which params support Jinja templating
    template_fields = ('table', 'sql')

    def __init__(
        self,
        table     : str,
        conn_id   : str,
        sql       : str,
        threshold : float = 0.0,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.table     = table
        self.conn_id   = conn_id
        self.sql       = sql
        self.threshold = threshold

    def execute(self, context):
        from airflow.providers.postgres.hooks.postgres import PostgresHook

        hook    = PostgresHook(postgres_conn_id=self.conn_id)
        records = hook.get_records(self.sql)

        if not records or records[0][0] < self.threshold:
            raise ValueError(
                f"Data quality check FAILED on {self.table}. "
                f"Got {records[0][0]}, expected >= {self.threshold}"
            )

        self.log.info(f"✅ Data quality check passed: {records[0][0]} rows")
        return records[0][0]


# ── Usage ──────────────────────────────────────────────────────
check_orders = DataQualityOperator(
    task_id   = 'check_orders_quality',
    table     = 'fct_orders',
    conn_id   = 'my_postgres',
    sql       = 'SELECT COUNT(*) FROM fct_orders WHERE order_date = {{ ds }}',
    threshold = 100,
)
```

---

## 7. Custom Hooks

> **Reusable connection layer for systems with no existing Airflow provider.**

```python
from airflow.hooks.base import BaseHook
import requests

class MyAPIHook(BaseHook):
    """
    Hook for a custom REST API.
    """
    conn_name_attr = 'my_api_conn_id'
    default_conn_name = 'my_api_default'

    def __init__(self, conn_id: str = default_conn_name):
        super().__init__()
        self.conn_id = conn_id
        self._session = None

    def get_conn(self):
        if self._session is None:
            conn = self.get_connection(self.conn_id)
            self._session = requests.Session()
            self._session.headers.update({
                'Authorization': f'Bearer {conn.password}',
                'Content-Type' : 'application/json',
            })
            self.base_url = f"http://{conn.host}:{conn.port}"
        return self._session

    def get_data(self, endpoint: str) -> dict:
        session  = self.get_conn()
        response = session.get(f"{self.base_url}/{endpoint}")
        response.raise_for_status()
        return response.json()


# ── Use Hook inside a PythonOperator ──────────────────────────
def fetch_from_api(**kwargs):
    hook = MyAPIHook(conn_id='my_api')
    data = hook.get_data('v1/orders')
    return len(data)
```

---

## 8. Testing DAGs

> **Three levels of testing: import, structure, logic.**

### Level 1 — DAG Import Test (catches syntax errors)

```python
# tests/test_dag_import.py
import pytest
from airflow.models import DagBag

def test_dag_bag_import():
    dag_bag = DagBag(dag_folder='dags/', include_examples=False)
    assert len(dag_bag.import_errors) == 0, \
        f"DAG import errors: {dag_bag.import_errors}"
```

### Level 2 — DAG Structure Tests

```python
def test_dag_structure():
    dag_bag = DagBag()
    dag     = dag_bag.get_dag('my_etl_dag')

    assert dag is not None
    assert len(dag.tasks) == 4

    task_ids = [t.task_id for t in dag.tasks]
    assert 'extract'   in task_ids
    assert 'transform' in task_ids
    assert 'load'      in task_ids

def test_dependencies():
    dag     = DagBag().get_dag('my_etl_dag')
    extract = dag.get_task('extract')

    assert dag.get_task('transform') in extract.downstream_list
```

### Level 3 — Task Logic Tests (unit test the callable)

```python
# Test the Python function, not the operator wrapper
def test_transform_logic():
    from dags.my_dag import transform_data

    raw = {'sales': [100, 200, 300], 'date': '2024-01-01'}
    result = transform_data(raw)

    assert result['total'] == 600
    assert result['avg']   == 200
```

### Run Tests

```bash
pytest tests/ -v
pytest tests/test_dag_import.py -v
```

---

## 9. Airflow + dbt Integration

> **Most common DE pattern: Airflow orchestrates dbt runs.**

```
Airflow DAG:
extract (Python) ──► dbt run (BashOperator) ──► dbt test ──► notify
```

```python
from airflow.operators.bash import BashOperator

dbt_run = BashOperator(
    task_id      = 'dbt_run',
    bash_command = '''
        cd /opt/dbt/my_project &&
        dbt run
          --profiles-dir /opt/dbt
          --target prod
          --models tag:daily
          --vars '{"run_date": "{{ ds }}"}'
    ''',
)

dbt_test = BashOperator(
    task_id      = 'dbt_test',
    bash_command = 'cd /opt/dbt/my_project && dbt test --profiles-dir /opt/dbt',
)

dbt_run >> dbt_test
```

### Using astronomer-cosmos (best practice 2024+)

```python
# cosmos renders each dbt model as an individual Airflow task
from cosmos import DbtDag, ProjectConfig, ProfileConfig

my_dbt_dag = DbtDag(
    project_config = ProjectConfig('/opt/dbt/my_project'),
    profile_config = ProfileConfig(
        profile_name      = 'my_project',
        target_name       = 'prod',
        profile_mapping   = SnowflakeUserPasswordProfileMapping(
            conn_id = 'snowflake_conn'
        ),
    ),
    schedule_interval = '@daily',
    start_date        = datetime(2024, 1, 1),
)
```

---

## 10. Airflow + Spark Integration

```python
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator

# ── Local / on-prem Spark ─────────────────────────────────────
spark_local = SparkSubmitOperator(
    task_id     = 'spark_transform',
    application = '/opt/spark/jobs/transform.py',
    conn_id     = 'spark_default',
    application_args = ['--date', '{{ ds }}'],
    conf = {
        'spark.executor.memory'  : '4g',
        'spark.executor.cores'   : '2',
        'spark.sql.shuffle.partitions': '200',
    },
)

# ── AWS Glue (serverless Spark) ───────────────────────────────
glue_job = GlueJobOperator(
    task_id       = 'run_glue_etl',
    job_name      = 'my-glue-transform',
    script_args   = {'--run_date': '{{ ds }}'},
    aws_conn_id   = 'my_aws',
    deferrable    = True,   # release worker slot while Glue runs
)

# ── GCP Dataproc ──────────────────────────────────────────────
dataproc_job = DataprocSubmitJobOperator(
    task_id    = 'dataproc_spark',
    project_id = 'my-gcp-project',
    region     = 'us-central1',
    job = {
        'placement': {'cluster_name': 'my-cluster'},
        'pyspark_job': {'main_python_file_uri': 'gs://bucket/jobs/transform.py'},
    },
)
```

---

## 11. Airflow on AWS (MWAA)

> **MWAA = Managed Workflows for Apache Airflow — fully managed by AWS.**

```
MWAA Architecture:
S3 bucket (dags/) ──► MWAA Environment ──► executes tasks
                          │
                          ├── Auto-scaling workers
                          ├── Managed scheduler
                          ├── VPC networking
                          └── IAM-based auth
```

### Key MWAA Differences vs Self-hosted

| | Self-hosted | MWAA |
|--|-------------|------|
| Setup | Manual | Managed |
| Executor | Configurable | CeleryExecutor (managed) |
| Scaling | Manual | Auto (min/max workers) |
| DAG deployment | Copy to server | Upload to S3 |
| Auth | Username/password | AWS IAM / SSO |
| Cost | Infra only | Managed service fee + infra |

```python
# MWAA-specific: use IAM roles instead of stored credentials
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

# No conn_id needed if MWAA has IAM role attached
hook = S3Hook()  # uses instance role automatically
```

---

## 12. Production Best Practices

```
✅ DO                                    ❌ DON'T
─────────────────────────────────────────────────────────────
Set catchup=False                        Leave catchup=True
Use max_active_runs=1 for ETLs           Allow concurrent DAG runs
Set execution_timeout on tasks           Let tasks run forever
Use reschedule mode for long sensors     Use poke mode for hours
Pass file paths via XCom                 Pass DataFrames via XCom
Store secrets in Vault/Secrets Manager   Store in Variables plaintext
Use Task Groups for UI organisation      Use SubDAGs
Version control DAG files in Git         Edit DAGs directly in prod
Use tags for DAG discovery               Leave tags empty
Parameterise DAGs with Variables         Hardcode env-specific values
Test DAGs with pytest before deploy      Deploy untested DAGs
Set email_on_failure in default_args     Rely only on UI monitoring
Use @task decorator for Python tasks     Boilerplate PythonOperator
```

---

## 13. Common Pitfalls & Fixes

### Pitfall 1: DAG parsing is too slow

```
Problem:  DB queries or API calls at module level (outside tasks)
Effect:   Scheduler slows down — parses every 30 seconds

❌ BAD:
import psycopg2
conn = psycopg2.connect(...)       # runs at parse time!
tables = conn.execute("SELECT...") # runs at parse time!

✅ FIX:
def extract(**kwargs):
    conn = psycopg2.connect(...)   # runs at task execution time
    tables = conn.execute(...)
```

---

### Pitfall 2: Timezone confusion

```python
# ❌ BAD — naive datetime (no timezone)
start_date = datetime(2024, 1, 1)

# ✅ GOOD — timezone-aware
from pendulum import datetime
start_date = datetime(2024, 1, 1, tz='Asia/Kolkata')
```

---

### Pitfall 3: XCom with large data

```python
# ❌ BAD — pushing DataFrame via XCom
def extract(**kwargs):
    df = pd.read_csv('/data/large_file.csv')   # 500MB
    kwargs['ti'].xcom_push(key='data', value=df.to_dict())  # 💥 DB overflow

# ✅ FIX — push S3 path
def extract(**kwargs):
    df = pd.read_csv('/data/large_file.csv')
    df.to_parquet('s3://my-bucket/tmp/extract_{{ ds }}.parquet')
    kwargs['ti'].xcom_push(key='s3_path', value='s3://my-bucket/tmp/extract_{{ ds }}.parquet')
```

---

### Pitfall 4: Task depends on global state

```python
# ❌ BAD — mutable global variable
counter = 0

def increment(**kwargs):
    global counter
    counter += 1   # workers are separate processes — this doesn't work!

# ✅ FIX — use XCom or external storage
def increment(**kwargs):
    ti    = kwargs['ti']
    count = ti.xcom_pull(task_ids='prev_task', key='count') or 0
    ti.xcom_push(key='count', value=count + 1)
```

---

### Pitfall 5: Not setting max_active_runs

```python
# ❌ DAG runs pile up if each run takes longer than schedule
with DAG('hourly_etl', schedule_interval='@hourly', ...) as dag: ...
# If one run takes 2 hours → 2 runs overlap → DB conflicts

# ✅ FIX
with DAG('hourly_etl', schedule_interval='@hourly',
         max_active_runs=1, ...) as dag: ...
```

---

## 14. Performance Tuning

### Scheduler Tuning (`airflow.cfg`)

```ini
[scheduler]
# How often scheduler parses DAG files (seconds)
min_file_process_interval = 30

# How many DAG files to parse in parallel
parsing_processes = 4

# How often scheduler checks for tasks to queue (seconds)
scheduler_heartbeat_sec = 5

[core]
# Max tasks running across all DAGs
parallelism = 32

# Max tasks running per DAG
max_active_tasks_per_dag = 16

# Max concurrent DAG runs per DAG
max_active_runs_per_dag = 1
```

### Worker Tuning (Celery)

```ini
[celery]
worker_concurrency = 16    # tasks per worker process
```

### DAG-level Optimisation

```python
with DAG(
    dag_id            = 'optimised_dag',
    max_active_tasks  = 8,     # limit parallelism within this DAG
    max_active_runs   = 1,     # no concurrent runs
    dagrun_timeout    = timedelta(hours=2),  # kill stale runs
    ...
) as dag:
    ...
```

---

## 15. Advanced DE Interview Q&A ⚡

> **Q: How do you build a dynamic DAG that processes a new table without code change?**
> Store table list in a JSON config file or Airflow Variable. Parse it at DAG definition time and loop to generate tasks. Add a new entry to config — new task appears on next scheduler parse.

> **Q: What is the DAG factory pattern?**
> A Python function that takes parameters and returns a complete DAG object. Call it multiple times with different configs to generate multiple DAGs — avoids code duplication.

> **Q: How do you handle backfilling safely in production?**
> Use `airflow dags backfill` with explicit `--start-date` and `--end-date`. Set `max_active_runs=1` to prevent overlap. Test on non-prod first. Use `--dry-run` to preview.

> **Q: What is a Deferrable Operator and why does it matter for cost?**
> Releases the worker slot while waiting for an external system (Spark, Glue, BigQuery). At scale, this means fewer workers needed — direct infra cost saving.

> **Q: How do you implement alerting in Airflow?**
> `on_failure_callback` on tasks or DAG level. Callbacks receive full context (dag_id, task_id, exception). Send to Slack via webhook, PagerDuty via API, or email via EmailOperator.

> **Q: How do you integrate Airflow with dbt?**
> Option 1: `BashOperator` running `dbt run`. Option 2: `astronomer-cosmos` library — renders each dbt model as a separate Airflow task with full lineage in UI.

> **Q: How do you test DAGs before deploying?**
> Three levels: (1) Import test via DagBag — catches syntax errors. (2) Structure tests — verify tasks, dependencies. (3) Unit tests on Python callables — test business logic directly.

> **Q: What's the difference between a Dataset and a schedule_interval?**
> `schedule_interval` = time-based trigger (every day at 6 AM).
> Dataset = event-based trigger (run when upstream data is updated). Datasets create data-aware pipelines — consumer runs only when producer actually finishes.

> **Q: How do you deploy DAGs in a production MWAA setup?**
> Push DAG files to the configured S3 bucket. MWAA syncs from S3 automatically. No server access needed. Use CI/CD pipeline (GitHub Actions) to push to S3 on merge to main.

> **Q: What causes a zombie task in Airflow?**
> A task that is in `running` state in the DB but whose worker process has died. The scheduler detects zombie tasks periodically and marks them as failed. Causes: worker crash, OOM kill, network partition.

> **Q: How do you prevent a slow DAG from blocking others?**
> Use Pools to cap its slot usage. Set `execution_timeout` on slow tasks. Set `max_active_tasks` on the DAG. Use priority_weight to deprioritise it.

> **Q: What is priority_weight in Airflow?**
> Controls task scheduling order when multiple tasks compete for slots. Higher number = scheduled first. Useful when some pipelines are more critical than others.

```python
critical_task = PythonOperator(
    task_id         = 'critical_load',
    python_callable = load_fn,
    priority_weight = 10,   # high priority
    weight_rule     = 'absolute',
)
```

---

*⚙️ Airflow Advanced · Production patterns · DE-interview complete coverage*
