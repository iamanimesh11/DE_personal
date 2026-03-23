# 📘 Apache Airflow — Theory & Concepts

> Architecture · Core concepts · How things work internally · Interview Q&A

---

## 📑 Table of Contents

| # | Topic |
|---|-------|
| 1 | [What is Airflow & Why](#1-what-is-airflow--why) |
| 2 | [Airflow Architecture](#2-airflow-architecture) |
| 3 | [DAG — Deep Dive](#3-dag--deep-dive) |
| 4 | [Task Lifecycle & States](#4-task-lifecycle--states) |
| 5 | [Executors](#5-executors) |
| 6 | [Operators vs Sensors vs Hooks](#6-operators-vs-sensors-vs-hooks) |
| 7 | [XCom — How it Works Internally](#7-xcom--how-it-works-internally) |
| 8 | [Scheduling — How it Works](#8-scheduling--how-it-works) |
| 9 | [Connections & Variables Internals](#9-connections--variables-internals) |
| 10 | [Trigger Rules](#10-trigger-rules) |
| 11 | [Pools & Concurrency](#11-pools--concurrency) |
| 12 | [Task Groups](#12-task-groups) |
| 13 | [SubDAGs vs Task Groups](#13-subdags-vs-task-groups) |
| 14 | [Airflow vs Other Orchestrators](#14-airflow-vs-other-orchestrators) |
| 15 | [Interview Q&A Fire Round](#15-interview-qa-fire-round-) |

---

## 1. What is Airflow & Why

```
Without Airflow:
cron job 1 → cron job 2 → cron job 3
  ↑               ↑              ↑
No visibility  No retry    No dependency
No alerting   No history   management
```

```
With Airflow:
┌───────────────────────────────────────────┐
│              Apache Airflow               │
│                                           │
│  extract ──► transform ──► load ──► notify│
│     ↑            ↑           ↑        ↑  │
│  retry 3x    retry 3x    retry 3x   email│
│  logs ✅     logs ✅      logs ✅    alert│
└───────────────────────────────────────────┘
```

> **What is Airflow?**
> An open-source platform to **author, schedule, and monitor** workflows as Directed Acyclic Graphs (DAGs) written in Python.

> **Key characteristics:**
> - Workflows as code (Python) — version controllable
> - Rich UI for monitoring and debugging
> - Extensible with 1000+ operators/providers
> - Not a data streaming tool (that's Kafka/Spark Streaming)
> - Not a data transformation tool (that's dbt/Spark)
> - It is purely an **orchestrator** — tells other systems what to do and when

> **Q: What problems does Airflow solve?**
> Dependency management between tasks, retry logic, alerting, scheduling, visibility into pipeline health — all in one place.

---

## 2. Airflow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AIRFLOW COMPONENTS                        │
│                                                             │
│  ┌──────────┐    ┌───────────┐    ┌──────────────────────┐ │
│  │Webserver │    │ Scheduler │    │      Executor        │ │
│  │          │    │           │    │  ┌────────────────┐  │ │
│  │ UI/API   │    │ Parses    │    │  │ Worker 1       │  │ │
│  │ Monitor  │    │ DAGs      │    │  │ Worker 2       │  │ │
│  │ Trigger  │    │ Schedules │    │  │ Worker 3       │  │ │
│  │          │    │ Tasks     │    │  └────────────────┘  │ │
│  └──────────┘    └───────────┘    └──────────────────────┘ │
│        │               │                    │              │
│        └───────────────┴────────────────────┘              │
│                        │                                    │
│              ┌─────────▼──────────┐                        │
│              │   Metadata DB      │                        │
│              │ (PostgreSQL/MySQL) │                        │
│              │ DAG runs, task     │                        │
│              │ states, XComs,     │                        │
│              │ variables, conns   │                        │
│              └────────────────────┘                        │
│                        │                                    │
│              ┌─────────▼──────────┐                        │
│              │    DAG Folder      │                        │
│              │  /dags/*.py files  │                        │
│              └────────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Role |
|-----------|------|
| **Webserver** | Flask app — UI, REST API, user auth, manual triggers |
| **Scheduler** | Heartbeat loop — parses DAGs, schedules tasks, writes to DB |
| **Executor** | Determines HOW tasks are run (local, Celery, K8s) |
| **Worker** | Actually executes the task code |
| **Metadata DB** | Stores ALL state — runs, task instances, XComs, vars, conns |
| **DAG Folder** | Where `.py` DAG files live — scheduler parses them periodically |

> **Q: What happens when you trigger a DAG?**
```
1. Scheduler detects trigger (schedule or manual)
2. Creates a DagRun record in Metadata DB
3. Creates TaskInstance records for each task
4. Executor picks up queued TaskInstances
5. Worker runs the task code
6. Worker updates TaskInstance state in DB (success/failed)
7. Scheduler checks dependencies, queues next tasks
8. Webserver reads DB and shows live status in UI
```

---

## 3. DAG — Deep Dive

> **DAG = Directed Acyclic Graph**

```
Directed  → edges have direction (A → B, not B → A)
Acyclic   → no cycles (A → B → C → A is NOT allowed)
Graph     → nodes (tasks) connected by edges (dependencies)
```

```
✅ Valid DAG:              ❌ Invalid (has cycle):
extract ──► transform      A ──► B
               │                 ↑
               ▼                 │
             load ──► notify     C ◄── B   ← cycle!
```

### Key DAG Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `dag_id` | Unique name | `'daily_etl'` |
| `schedule_interval` | When to run | `'@daily'`, `'0 6 * * *'` |
| `start_date` | When scheduling begins | `datetime(2024, 1, 1)` |
| `catchup` | Backfill missed runs | `False` (recommended) |
| `max_active_runs` | Concurrent DAG runs | `1` (prevent overlap) |
| `max_active_tasks` | Concurrent tasks | `16` |
| `default_args` | Applied to all tasks | retries, email, owner |
| `tags` | UI filtering | `['etl', 'daily']` |
| `on_failure_callback` | Alert on DAG fail | Slack function |
| `dagrun_timeout` | Max DAG run time | `timedelta(hours=2)` |

> **Q: What is catchup and when should you disable it?**
> `catchup=True` means Airflow creates DAG runs for ALL dates between `start_date` and now.
> For a DAG with `start_date = 2020-01-01` and `catchup=True` run today — it would try to run **1400+ times**.
> Always set `catchup=False` in production unless you explicitly need backfill.

> **Q: Can two DAGs have the same dag_id?**
> ❌ No — dag_id must be globally unique. Duplicates cause one to silently override the other.

---

## 4. Task Lifecycle & States

```
Task States:
                    ┌─────────┐
                    │  none   │  (not yet queued)
                    └────┬────┘
                         │ scheduler picks it up
                    ┌────▼────┐
                    │ scheduled│
                    └────┬────┘
                         │ executor queues it
                    ┌────▼────┐
                    │  queued  │
                    └────┬────┘
                         │ worker picks it up
                    ┌────▼────┐
                    │ running  │
                    └────┬────┘
              ┌──────────┼──────────┐
         ┌────▼────┐ ┌───▼────┐ ┌──▼──────┐
         │ success │ │ failed │ │ skipped │
         └─────────┘ └───┬────┘ └─────────┘
                         │ if retries left
                    ┌────▼────┐
                    │  up for │
                    │  retry  │
                    └─────────┘
```

| State | Meaning |
|-------|---------|
| `none` | Not yet considered by scheduler |
| `scheduled` | Scheduler has queued it |
| `queued` | Sent to executor, waiting for worker |
| `running` | Worker is executing it |
| `success` | Completed without error |
| `failed` | Raised an exception, no retries left |
| `skipped` | BranchOperator chose a different path |
| `up_for_retry` | Failed, has retries remaining |
| `up_for_reschedule` | Sensor in reschedule mode, waiting |
| `deferred` | Async task waiting for trigger |
| `removed` | Task removed from DAG but old instance exists |

> **Q: What is the difference between a DagRun and a TaskInstance?**
> `DagRun` = one execution of the whole DAG (has a run_id).
> `TaskInstance` = one execution of one task within a DagRun.
> One DagRun has many TaskInstances.

---

## 5. Executors

> **The Executor decides HOW and WHERE tasks are run.**

```
Airflow
  └── Scheduler
        └── Executor ──► runs tasks via...
              ├── SequentialExecutor  → one by one, same process
              ├── LocalExecutor       → parallel, same machine
              ├── CeleryExecutor      → distributed, multiple machines
              └── KubernetesExecutor  → each task = one K8s pod
```

### Executor Comparison

| Executor | Parallelism | Use case | Needs |
|----------|-------------|----------|-------|
| `SequentialExecutor` | ❌ None (1 task at a time) | Dev / testing only | SQLite |
| `LocalExecutor` | ✅ Multi-process | Single machine production | PostgreSQL/MySQL |
| `CeleryExecutor` | ✅ Multi-machine | Large scale, many tasks | Redis/RabbitMQ + workers |
| `KubernetesExecutor` | ✅ Dynamic pods | Isolation, variable workloads | K8s cluster |

```
CeleryExecutor architecture:
Scheduler ──► Redis/RabbitMQ (queue) ──► Celery Worker 1
                                     ──► Celery Worker 2
                                     ──► Celery Worker 3
```

> **Q: What executor is used in production at scale?**
> `CeleryExecutor` (most common) or `KubernetesExecutor` (cloud-native).
> Never use `SequentialExecutor` in production — it can't run tasks in parallel.

> **Q: What is the difference between CeleryExecutor and KubernetesExecutor?**
> Celery = persistent worker processes waiting for tasks (like a pool).
> Kubernetes = spins up a fresh pod per task, then destroys it (more isolation, more overhead).

---

## 6. Operators vs Sensors vs Hooks

```
┌──────────────────────────────────────────────────────┐
│                   AIRFLOW PRIMITIVES                  │
│                                                      │
│  Operator   → DO something (run code, SQL, script)  │
│  Sensor     → WAIT for something (file, API, time)  │
│  Hook       → CONNECT to something (DB, S3, API)    │
│                                                      │
│  Operator uses Hook internally to talk to systems   │
└──────────────────────────────────────────────────────┘
```

| Primitive | Purpose | Example |
|-----------|---------|---------|
| **Operator** | Unit of work — executes an action | `PythonOperator`, `BashOperator` |
| **Sensor** | Waits for external condition | `FileSensor`, `HttpSensor` |
| **Hook** | Low-level interface to external system | `PostgresHook`, `S3Hook` |

```python
# Relationship example:
# S3ToRedshiftOperator internally uses:
#   → S3Hook (to read from S3)
#   → RedshiftSQLHook (to write to Redshift)
# You just configure the Operator — Hook is abstracted away
```

> **Q: When do you use a Hook directly instead of an Operator?**
> When no Operator exists for your use case, or you need custom logic inside a `PythonOperator`.
> You call the Hook manually inside your Python function.

---

## 7. XCom — How it Works Internally

```
XCom = Cross-Communication between tasks

Task A runs → return value stored in metadata DB as XCom
Task B runs → pulls from metadata DB by (dag_id, run_id, task_id, key)
```

```
Metadata DB: xcom table
┌──────────┬──────────┬──────────┬───────┬───────────┐
│ dag_id   │ run_id   │ task_id  │ key   │ value     │
├──────────┼──────────┼──────────┼───────┼───────────┤
│ my_dag   │ run_001  │ extract  │return │ 5000      │
│ my_dag   │ run_001  │ extract  │source │ 'mysql'   │
└──────────┴──────────┴──────────┴───────┴───────────┘
```

> **Q: What are XCom limitations?**
> XComs are stored in the metadata DB — not designed for large data.
> Recommended limit: **< 48KB** (varies by DB).
> For large data, push a **file path** (S3 key, GCS URI) via XCom, not the data itself.

> **Q: What is XCom Backend?**
> In Airflow 2.x you can configure a custom XCom backend (e.g. S3) to store large values outside the metadata DB.

---

## 8. Scheduling — How it Works

```
Timeline for schedule_interval='@daily', start_date=2024-01-01:

data_interval_start   data_interval_end   when task ACTUALLY runs
2024-01-01            2024-01-02          2024-01-02 00:00 ← after interval ends!
2024-01-02            2024-01-03          2024-01-03 00:00
2024-01-03            2024-01-04          2024-01-04 00:00
```

> ⚠️ **Most common Airflow confusion:**
> A DAG with `start_date = 2024-01-01` and `schedule_interval = @daily`
> **does NOT run on 2024-01-01**. It runs at the END of the first interval — i.e. `2024-01-02 00:00`.
> Airflow runs at the END of the period, not the beginning.

```python
# Key template variables for understanding schedule:
{{ ds }}              # data_interval_start date (the period being processed)
{{ data_interval_start }}  # start of processing window
{{ data_interval_end }}    # end of processing window (when task ran)
```

> **Q: What is `execution_date` in Airflow?**
> The `data_interval_start` — the logical date of the data being processed.
> In Airflow 2.2+ this is called `logical_date`. Same concept.

> **Q: What is the difference between `start_date` and `schedule_interval`?**
> `start_date` = the earliest date from which scheduling begins.
> `schedule_interval` = how often the DAG runs after that.

---

## 9. Connections & Variables Internals

```
Where are they stored?
  Connections → metadata DB (encrypted with Fernet key)
  Variables   → metadata DB (can be marked as secret)

Where else can they live?
  → Environment variables
  → AWS Secrets Manager
  → HashiCorp Vault
  → Google Secret Manager
```

```bash
# Connection as environment variable (no UI needed):
export AIRFLOW_CONN_MY_POSTGRES='postgresql://user:pass@host:5432/mydb'

# Variable as environment variable:
export AIRFLOW_VAR_ENVIRONMENT='production'
```

> **Q: Why use Secrets Manager over storing in Airflow metadata DB?**
> Metadata DB is not designed as a secrets store. For production:
> Use AWS Secrets Manager / Vault to avoid credentials in the DB.

> **Q: What is a Fernet key in Airflow?**
> A symmetric encryption key used to encrypt sensitive fields (passwords in connections).
> Without it, passwords are stored in plain text. Always configure in production.

---

## 10. Trigger Rules

> **By default, a task runs only when ALL upstream tasks succeed.**
> Trigger rules change this behaviour.

```
upstream tasks: [A, B, C]
                     ↓
                   task D  ← when does D run?
                   depends on trigger_rule
```

| Trigger Rule | D runs when... | Use case |
|--------------|---------------|----------|
| `all_success` *(default)* | All upstream succeed | Normal pipeline |
| `all_failed` | All upstream fail | Failure handler |
| `all_done` | All upstream complete (any state) | Cleanup task |
| `one_success` | At least one upstream succeeds | Race condition pattern |
| `one_failed` | At least one upstream fails | Alert on any failure |
| `none_failed` | None have failed (success or skip ok) | After branch join |
| `none_failed_min_one_success` | None failed + at least one success | Branch join ✅ |
| `always` | Regardless of upstream state | Notification tasks |

```python
# Common use — join after BranchPythonOperator
notify = EmptyOperator(
    task_id      = 'notify',
    trigger_rule = 'none_failed_min_one_success'
    # runs whether full_load OR incremental_load was chosen
)
```

---

## 11. Pools & Concurrency

> **Pools limit how many tasks can run simultaneously — for resource management.**

```
Without pool:              With pool (limit=2):
All 10 tasks run at once   Max 2 tasks run at once
→ DB overwhelmed           → DB protected ✅

┌──────────────────┐
│   my_db_pool     │  slots=2
│  ████░░░░░░░░    │  2 running, 8 waiting
└──────────────────┘
```

```python
# Create pool in UI (Admin → Pools) or CLI:
airflow pools set my_db_pool 5 "Limit DB connections"

# Assign task to pool:
extract = PythonOperator(
    task_id         = 'extract',
    python_callable = extract_fn,
    pool            = 'my_db_pool',
    pool_slots      = 1,           # how many slots this task consumes
)
```

### Concurrency Settings (hierarchy)

```
airflow.cfg: parallelism          → max tasks running across ALL DAGs
DAG:         max_active_tasks     → max tasks running in one DAG
DAG:         max_active_runs      → max concurrent runs of same DAG
Task:        pool                 → resource-based slot limiting
```

> **Q: How do you prevent a DAG from overlapping with itself?**
> Set `max_active_runs = 1` on the DAG — ensures only one run at a time.

---

## 12. Task Groups

> **Visual grouping of related tasks in the Airflow UI — replaces SubDAGs.**

```python
from airflow.utils.task_group import TaskGroup

with DAG('my_dag', ...) as dag:

    start = EmptyOperator(task_id='start')

    with TaskGroup('extract_group') as extract_grp:
        extract_orders  = PythonOperator(task_id='extract_orders',  ...)
        extract_users   = PythonOperator(task_id='extract_users',   ...)
        extract_products= PythonOperator(task_id='extract_products',...)

    with TaskGroup('transform_group') as transform_grp:
        clean    = PythonOperator(task_id='clean',    ...)
        validate = PythonOperator(task_id='validate', ...)

    end = EmptyOperator(task_id='end')

    start >> extract_grp >> transform_grp >> end
```

```
UI view:
start ──► [extract_group] ──► [transform_group] ──► end
               ↕ expand                ↕ expand
          extract_orders          clean
          extract_users           validate
          extract_products
```

---

## 13. SubDAGs vs Task Groups

| | SubDAG | Task Group |
|--|--------|------------|
| Available since | Airflow 1.x | Airflow 2.0 |
| Implementation | Separate DAG object | Logical grouping only |
| Executor | Uses SequentialExecutor ⚠️ | Uses parent DAG's executor ✅ |
| Deadlock risk | ✅ Yes (pool exhaustion) | ❌ No |
| UI support | Limited | Collapsible groups ✅ |
| Recommended? | ❌ Deprecated | ✅ Use this |

> **Q: Why were SubDAGs deprecated?**
> SubDAGs ran on `SequentialExecutor` by default (no parallelism) and could cause
> deadlocks when the parent DAG ran out of worker slots waiting for the SubDAG.
> Task Groups solve the same problem with none of these issues.

---

## 14. Airflow vs Other Orchestrators

```
┌─────────────────────────────────────────────────────────┐
│             ORCHESTRATOR COMPARISON                      │
├────────────────┬────────────┬──────────┬────────────────┤
│                │  Airflow   │  Prefect │  Dagster       │
├────────────────┼────────────┼──────────┼────────────────┤
│ DAG definition │ Python     │ Python   │ Python         │
│ Dynamic DAGs   │ Limited    │ ✅ Easy  │ ✅ Easy        │
│ Local dev      │ Complex    │ ✅ Easy  │ ✅ Easy        │
│ Observability  │ Basic UI   │ Good     │ ✅ Best        │
│ Maturity       │ ✅ Most    │ Growing  │ Growing        │
│ Community      │ ✅ Largest │ Good     │ Good           │
│ Cloud managed  │ MWAA,      │ Prefect  │ Dagster Cloud  │
│                │ Cloud Comp │ Cloud    │                │
├────────────────┼────────────┼──────────┼────────────────┤
│ Best for       │ Traditional│ Modern   │ Data-aware     │
│                │ pipelines  │ Python   │ pipelines      │
└────────────────┴────────────┴──────────┴────────────────┘
```

> **Q: Airflow vs Spark — what's the difference?**
> Airflow = **orchestrator** (schedules and coordinates work).
> Spark = **processing engine** (does the actual computation).
> They are used together — Airflow DAG triggers a Spark job via `SparkSubmitOperator`.

> **Q: Airflow vs Kafka — what's the difference?**
> Airflow = batch workflow orchestration (minutes to hours granularity).
> Kafka = real-time event streaming (millisecond granularity).
> Not competitors — different tools for different problems.

---

## 15. Interview Q&A Fire Round ⚡

> **Q: What is a DAG in Airflow?**
> A Directed Acyclic Graph — a Python file that defines a workflow as a set of tasks with dependencies. No cycles allowed.

> **Q: What is the metadata database used for?**
> Stores DAG definitions, task states, XComs, connections, variables, user info, run history — everything Airflow needs to operate.

> **Q: What happens if the scheduler goes down?**
> Running tasks continue on workers. New tasks won't be scheduled. DAG runs won't be triggered. Recovering the scheduler resumes normal operation.

> **Q: What is the difference between a DAG run and a task instance?**
> DAG run = one execution of the whole DAG. Task instance = one execution of one task within a DAG run.

> **Q: What is catchup in Airflow?**
> When `catchup=True`, Airflow creates DAG runs for every missed interval between `start_date` and now. Set `catchup=False` to prevent accidental backfills.

> **Q: When does a daily DAG with start_date=Jan 1 actually first run?**
> Jan 2 — Airflow runs at the END of the scheduled interval, not the beginning.

> **Q: What is the difference between poke and reschedule mode in sensors?**
> Poke = holds a worker slot while waiting (bad for long waits).
> Reschedule = releases worker slot between checks (efficient for long waits).

> **Q: What are trigger rules? Give an example.**
> Controls when a task runs relative to upstream states. `none_failed_min_one_success` is used after BranchPythonOperator to run a join task regardless of which branch executed.

> **Q: What is the purpose of pools in Airflow?**
> Limit concurrent tasks that use a shared resource (e.g. max 5 DB connections). Prevents overloading external systems.

> **Q: How do you pass data between tasks?**
> Via XCom — but only for small values (IDs, paths, counts). For large data, use external storage (S3, GCS) and pass the path via XCom.

> **Q: What executor is best for production?**
> `CeleryExecutor` for multi-machine scale. `KubernetesExecutor` for dynamic, isolated workloads.

> **Q: How do you handle a slow task blocking the whole pipeline?**
> Set `execution_timeout` on the task + appropriate `retries`. Use pools to prevent it consuming too many slots.

> **Q: What is the difference between Variables and Connections?**
> Variables = key-value config store (env, paths, settings).
> Connections = credentials + endpoint info for external systems (DB host, port, password).

> **Q: What is a Fernet key?**
> Encryption key for sensitive fields in the metadata DB (passwords). Always configure in production.

> **Q: Why use Task Groups instead of SubDAGs?**
> SubDAGs use SequentialExecutor (no parallelism) and can deadlock. Task Groups are purely UI-level grouping with no execution overhead.

---

*📘 Airflow Theory · Architecture · Internals · Interview-ready*
