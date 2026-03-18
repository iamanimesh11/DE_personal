# ⚙️ SQL for Data Engineering — Advanced Cheatsheet

> Topics **not** in sqltheory.md or sql_commands.md
> DE-interview focused · Diagrams + Real examples · 100% coverage

---

## 📑 Table of Contents

| # | Topic |
|---|-------|
| 1 | [ETL vs ELT](#1-etl-vs-elt) |
| 2 | [Partitioning](#2-partitioning) |
| 3 | [Slowly Changing Dimensions (SCD)](#3-slowly-changing-dimensions-scd) |
| 4 | [Data Types — Choosing Right](#4-data-types--choosing-right) |
| 5 | [Temp Tables vs CTEs vs Subqueries](#5-temp-tables-vs-ctes-vs-subqueries) |
| 6 | [INTERSECT & EXCEPT](#6-intersect--except) |
| 7 | [PIVOT & UNPIVOT](#7-pivot--unpivot) |
| 8 | [JSON in SQL](#8-json-in-sql) |
| 9 | [Query Optimization Patterns](#9-query-optimization-patterns) |
| 10 | [AUTO_INCREMENT & Sequences](#10-auto_increment--sequences) |
| 11 | [Data Quality Checks in SQL](#11-data-quality-checks-in-sql) |
| 12 | [Incremental Load Patterns](#12-incremental-load-patterns) |
| 13 | [Surrogate Keys in Data Warehouses](#13-surrogate-keys-in-data-warehouses) |
| 14 | [Bucketing vs Partitioning](#14-bucketing-vs-partitioning) |
| 15 | [DE Interview Fire Round](#15-de-interview-fire-round-) |

---

## 1. ETL vs ELT

```
ETL (Traditional):
Source → [ Extract ] → [ Transform ] → [ Load ] → Data Warehouse
         raw data      clean/reshape    final      (on-prem, SQL Server)

ELT (Modern Cloud):
Source → [ Extract ] → [ Load ] → [ Transform ] → Data Warehouse
         raw data       raw dump    SQL inside DWH  (Redshift, BigQuery, Snowflake)
```

| | ETL | ELT |
|--|-----|-----|
| Transform happens | Before loading | After loading |
| Tool does transform | Spark, Glue, Informatica | SQL inside DWH |
| Best for | Sensitive data, complex logic | Cloud DWH, large scale |
| Storage cost | Low (only clean data loaded) | Higher (raw data stored first) |
| Flexibility | Less (schema defined upfront) | More (raw data always available) |
| Example tools | AWS Glue, SSIS, Talend | dbt, BigQuery, Redshift |

> **Q: Why is ELT preferred in modern data engineering?**
> Cloud DWHs (BigQuery, Redshift) are massively parallel — transforming data INSIDE them
> is faster and cheaper than moving it to an external engine first.

> **Q: What is dbt (data build tool)?**
> A framework for writing ELT transforms as SQL `SELECT` statements with version control,
> lineage, and testing built in. Sits on top of your DWH.

```
dbt flow:
raw_orders (source) → stg_orders (staging) → fct_orders (final fact table)
                            ↑ all written as SQL SELECT models in dbt
```

---

## 2. Partitioning

> **Splitting a large table into smaller physical chunks for faster queries.**
> Instead of scanning 1 billion rows — scan only the partition you need.

```
orders table (1 billion rows)
┌─────────────────────────────────────────┐
│  Partition 2022  │  Partition 2023  │  Partition 2024  │
│  (300M rows)     │  (400M rows)     │  (300M rows)     │
└─────────────────────────────────────────┘
        ↑
WHERE order_year = 2024 → only scans 300M rows, not 1 billion
```

---

### Partition Types

#### RANGE Partitioning — most common for dates/numbers

```sql
CREATE TABLE orders (
  order_id   INT,
  order_date DATE,
  amount     DECIMAL
)
PARTITION BY RANGE (YEAR(order_date)) (
  PARTITION p2022 VALUES LESS THAN (2023),
  PARTITION p2023 VALUES LESS THAN (2024),
  PARTITION p2024 VALUES LESS THAN (2025),
  PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

#### LIST Partitioning — for known discrete values

```sql
PARTITION BY LIST (region) (
  PARTITION p_north VALUES IN ('Delhi', 'Punjab', 'UP'),
  PARTITION p_south VALUES IN ('Chennai', 'Bangalore', 'Kochi'),
  PARTITION p_west  VALUES IN ('Mumbai', 'Pune', 'Ahmedabad')
);
```

#### HASH Partitioning — for even distribution, no natural key

```sql
PARTITION BY HASH (customer_id)
PARTITIONS 4;
-- Distributes rows evenly across 4 partitions based on hash of customer_id
```

#### COMPOSITE Partitioning — RANGE + HASH together

```sql
PARTITION BY RANGE (YEAR(order_date))
  SUBPARTITION BY HASH (customer_id) SUBPARTITIONS 4 (
  PARTITION p2023 VALUES LESS THAN (2024),
  PARTITION p2024 VALUES LESS THAN (2025)
);
```

---

### Partitioning Quick Reference

| Type | Best for | Example column |
|------|----------|---------------|
| RANGE | Dates, time series, numeric ranges | `order_date`, `age` |
| LIST | Known categories, regions | `country`, `status` |
| HASH | Even distribution, no natural key | `user_id`, `order_id` |
| COMPOSITE | Huge tables needing both | date + customer_id |

> **Q: What is partition pruning?**
> When the query optimizer skips irrelevant partitions entirely.
> `WHERE order_date = '2024-01-01'` → only scans 2024 partition. 🟢

> **Q: What is partition elimination?**
> Same as pruning — the DB "eliminates" partitions that can't match the WHERE clause.

> **Q: Downside of over-partitioning?**
> Too many small partitions = metadata overhead + slower writes.
> Rule of thumb: each partition should be at least a few GB.

---

## 3. Slowly Changing Dimensions (SCD)

> **How do you handle changes to dimension data over time in a data warehouse?**
> e.g. A customer moves city. Do you overwrite? Keep history? Both?

```
dim_customer table — customer moves from Delhi to Mumbai

SCD Type 1 → Just overwrite. No history kept.
SCD Type 2 → Add a new row. Full history kept.
SCD Type 3 → Add a new column. Only previous value kept.
```

---

### SCD Type 1 — Overwrite (no history)

```sql
-- Customer moved from Delhi to Mumbai
UPDATE dim_customer
SET city = 'Mumbai'
WHERE customer_id = 101;

-- Before:  101 | Animesh | Delhi
-- After:   101 | Animesh | Mumbai   ← Delhi is gone forever
```

**Use when:** History doesn't matter (e.g. fixing a typo, phone number)

---

### SCD Type 2 — Add new row (full history) ✅ most common in DWH

```sql
-- Step 1: Expire the old record
UPDATE dim_customer
SET is_current = FALSE,
    valid_to   = CURRENT_DATE
WHERE customer_id = 101 AND is_current = TRUE;

-- Step 2: Insert new record
INSERT INTO dim_customer
  (customer_id, name, city, valid_from, valid_to, is_current)
VALUES
  (101, 'Animesh', 'Mumbai', CURRENT_DATE, '9999-12-31', TRUE);
```

```
customer_id  name      city     valid_from   valid_to     is_current
101          Animesh   Delhi    2020-01-01   2024-03-17   FALSE   ← old
101          Animesh   Mumbai   2024-03-18   9999-12-31   TRUE    ← current
```

**Use when:** Full history is needed (e.g. sales analysis by customer's city at time of purchase)

---

### SCD Type 3 — Add column (previous value only)

```sql
ALTER TABLE dim_customer ADD COLUMN prev_city VARCHAR(50);

UPDATE dim_customer
SET prev_city = city,
    city      = 'Mumbai'
WHERE customer_id = 101;

-- Result: 101 | Animesh | Mumbai | Delhi
--                 current  previous (only one level of history)
```

**Use when:** Only "before and after" matters, not full history

---

### SCD Summary

| Type | Stores history? | How | Use case |
|------|----------------|-----|----------|
| Type 1 | ❌ No | Overwrite | Typo fixes, non-analytical data |
| Type 2 | ✅ Full | New row per change | Customer address, product category |
| Type 3 | ⚠️ Partial | New column | Limited "before/after" tracking |

> **Q: What columns are typically added for SCD Type 2?**
> `valid_from`, `valid_to`, `is_current` (or `surrogate_key` as new PK)

> **Q: How do you query only current records in SCD Type 2?**
> `WHERE is_current = TRUE` or `WHERE valid_to = '9999-12-31'`

---

## 4. Data Types — Choosing Right

> **Wrong data type = wasted storage + slow queries + wrong results.**
> This is asked directly in DE schema design rounds.

---

### Numeric Types

```
INT        → -2.1B to 2.1B       (4 bytes)  — order_id, age
BIGINT     → -9.2 quintillion    (8 bytes)  — user_id at scale, timestamps
SMALLINT   → -32K to 32K         (2 bytes)  — status codes, small counters
TINYINT    → 0 to 255            (1 byte)   — boolean flags, ratings (1-5)
DECIMAL(p,s) → exact precision   — money, prices ✅ never use FLOAT for money!
FLOAT/DOUBLE → approximate       — scientific, not financial ⚠️
```

```
❌ WRONG: price FLOAT      → 99.99 stored as 99.98999786...
✅ RIGHT:  price DECIMAL(10,2) → 99.99 stored exactly
```

---

### String Types

```
VARCHAR(n)  → Variable length up to n chars  — names, emails, cities
CHAR(n)     → Fixed length always n chars    — country codes ('IN', 'US')
TEXT        → Large text, no length limit    — descriptions, logs
ENUM        → Predefined list of values      — status ('Active','Inactive')
```

```
CHAR(3) for 'IN'  → stores 'IN ' (padded) — always 3 bytes
VARCHAR(3) for 'IN' → stores 'IN' — 2 bytes (efficient)

✅ Use CHAR for fixed-length codes (ISO codes, status flags)
✅ Use VARCHAR for everything else
```

---

### Date / Time Types

```
DATE        → '2024-03-17'                   — just the date
TIME        → '14:30:00'                     — just the time
DATETIME    → '2024-03-17 14:30:00'          — date + time, no timezone
TIMESTAMP   → '2024-03-17 14:30:00 UTC'      — date + time WITH timezone ✅
YEAR        → '2024'                         — just the year
```

> **Q: DATETIME vs TIMESTAMP — which to use?**
> Use `TIMESTAMP` for event tracking — it stores UTC and converts to local timezone.
> Use `DATETIME` when you want timezone-agnostic values (e.g. scheduled run times).

---

### Boolean

```sql
-- MySQL: no native BOOLEAN — use TINYINT(1)
is_active TINYINT(1) DEFAULT 1    -- 1 = TRUE, 0 = FALSE

-- PostgreSQL: native BOOLEAN
is_active BOOLEAN DEFAULT TRUE
```

---

### Data Type Decision Guide

```
Is it money?          → DECIMAL(p,s)       never FLOAT
Is it a large ID?     → BIGINT             not INT (overflow at 2.1B)
Is it a fixed code?   → CHAR(n)            not VARCHAR
Is it a timestamp?    → TIMESTAMP          not DATETIME (for UTC events)
Is it a category?     → ENUM or VARCHAR    not INT codes
Is it a flag?         → TINYINT(1)         or BOOLEAN
Is it long text?      → TEXT               not VARCHAR(5000)
```

---

## 5. Temp Tables vs CTEs vs Subqueries

> **Three ways to break down a complex query — each with different tradeoffs.**

```
Subquery  → inline, single use, hardest to read
CTE       → named, reusable in same query, clean
Temp Table → physically stored, reusable across queries, fastest for big data
```

---

### Subquery

```sql
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) rn
  FROM employees
) t
WHERE rn = 1;
-- ✅ Simple cases  ❌ Can't reuse  ❌ Hard to debug
```

---

### CTE

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) rn
  FROM employees
),
top_earners AS (
  SELECT * FROM ranked WHERE rn = 1
)
SELECT * FROM top_earners WHERE salary > 80000;
-- ✅ Readable  ✅ Reusable in same query  ❌ Not persistent
```

---

### Temp Table

```sql
-- Create and populate
CREATE TEMPORARY TABLE tmp_ranked AS
SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) rn
FROM employees;

-- Reuse across multiple queries in same session
SELECT * FROM tmp_ranked WHERE rn = 1;
SELECT dept, COUNT(*) FROM tmp_ranked GROUP BY dept;

-- Auto-dropped when session ends
-- ✅ Fastest for large intermediate results  ✅ Reusable  ❌ Session-scoped only
```

---

### Decision Guide

| | Subquery | CTE | Temp Table |
|--|----------|-----|------------|
| Readability | ❌ Low | ✅ High | ✅ High |
| Reusable in same query | ❌ No | ✅ Yes | ✅ Yes |
| Reusable across queries | ❌ No | ❌ No | ✅ Yes |
| Materialized (stored) | ❌ No | ❌ No* | ✅ Yes |
| Best for | Simple inline | Complex readable | Large intermediate sets |

> *Some DBs (PostgreSQL) materialize CTEs, others re-evaluate each time.

> **Q: When do you prefer Temp Table over CTE in a pipeline?**
> When the intermediate result is large and used multiple times — temp table
> computes once and caches. CTE may re-execute each time it's referenced.

---

## 6. INTERSECT & EXCEPT

> **Set operations — complete the UNION family.**

```
Table A: [1, 2, 3, 4]
Table B: [3, 4, 5, 6]

UNION     → [1,2,3,4,5,6]   all unique rows from both
UNION ALL → [1,2,3,4,3,4,5,6] all rows including dupes
INTERSECT → [3,4]            only rows in BOTH
EXCEPT    → [1,2]            rows in A but NOT in B
```

---

### INTERSECT — rows that exist in both

```sql
-- Customers who placed orders AND made payments
SELECT customer_id FROM orders
INTERSECT
SELECT customer_id FROM payments;
```

---

### EXCEPT — rows in first query but not second

```sql
-- Customers who placed orders but NEVER made a payment
SELECT customer_id FROM orders
EXCEPT
SELECT customer_id FROM payments;

-- Same result using LEFT JOIN (alternative):
SELECT o.customer_id
FROM orders o
LEFT JOIN payments p ON o.customer_id = p.customer_id
WHERE p.customer_id IS NULL;
```

---

### Set Operations Quick Reference

| Operation | Returns | Duplicates |
|-----------|---------|------------|
| `UNION` | All rows from A + B | Removed |
| `UNION ALL` | All rows from A + B | Kept |
| `INTERSECT` | Rows in both A and B | Removed |
| `EXCEPT` / `MINUS` | Rows in A not in B | Removed |

> **Q: EXCEPT vs NOT IN vs LEFT JOIN anti-pattern?**
> All three find "missing" rows but `EXCEPT` is cleanest.
> `NOT IN` fails silently if subquery returns a NULL — use `NOT EXISTS` instead.

```sql
-- ⚠️ Dangerous if payments has NULL customer_id:
WHERE customer_id NOT IN (SELECT customer_id FROM payments)

-- ✅ Safer:
WHERE NOT EXISTS (SELECT 1 FROM payments p WHERE p.customer_id = o.customer_id)
```

---

## 7. PIVOT & UNPIVOT

> **Rotate rows into columns (PIVOT) or columns into rows (UNPIVOT).**
> Common in reporting, building wide feature tables, and data reshaping.

---

### PIVOT — rows → columns

```
Before (tall):                After (wide / pivoted):
month    product  sales       month   TV     Phone  Laptop
Jan      TV       500         Jan     500    300    200
Jan      Phone    300         Feb     400    600    350
Jan      Laptop   200
Feb      TV       400  ...
```

```sql
-- MySQL: simulate PIVOT using conditional aggregation
SELECT
  month,
  SUM(CASE WHEN product = 'TV'     THEN sales ELSE 0 END) AS TV,
  SUM(CASE WHEN product = 'Phone'  THEN sales ELSE 0 END) AS Phone,
  SUM(CASE WHEN product = 'Laptop' THEN sales ELSE 0 END) AS Laptop
FROM sales
GROUP BY month;
```

---

### UNPIVOT — columns → rows

```
Before (wide):                After (tall / unpivoted):
emp_id  Q1    Q2    Q3        emp_id  quarter  revenue
1       100   200   150       1       Q1       100
                              1       Q2       200
                              1       Q3       150
```

```sql
-- MySQL: simulate UNPIVOT using UNION ALL
SELECT emp_id, 'Q1' AS quarter, Q1 AS revenue FROM quarterly_sales
UNION ALL
SELECT emp_id, 'Q2', Q2 FROM quarterly_sales
UNION ALL
SELECT emp_id, 'Q3', Q3 FROM quarterly_sales;
```

> **Q: When is PIVOT used in data engineering?**
> Building feature tables for ML, creating wide reporting tables, and
> reshaping event data (one-row-per-event → one-row-per-user with columns per event type).

---

## 8. JSON in SQL

> **Modern data engineering deals with semi-structured data constantly.**
> APIs, Kafka events, and logs all produce JSON.

---

### Storing JSON

```sql
CREATE TABLE events (
  event_id   INT PRIMARY KEY,
  user_id    INT,
  payload    JSON           -- native JSON column
);

INSERT INTO events VALUES (1, 101, '{"action":"click","page":"home","duration":5}');
```

---

### Extracting JSON fields

```sql
-- Extract a value (returns string)
SELECT JSON_EXTRACT(payload, '$.action') FROM events;
-- Result: "click"

-- Shorthand operator (MySQL 5.7+)
SELECT payload->>'$.action' FROM events;
-- Result: click  (without quotes)

-- Nested path
SELECT payload->>'$.metadata.browser' FROM events;
```

---

### JSON Array operations

```sql
-- Get array element by index
SELECT JSON_EXTRACT(payload, '$.tags[0]') FROM events;

-- Get array length
SELECT JSON_LENGTH(payload->'$.tags') FROM events;
```

---

### Aggregating into JSON

```sql
-- Build JSON object per row
SELECT JSON_OBJECT('name', name, 'salary', salary) FROM employees;
-- Result: {"name": "Animesh", "salary": 95000}

-- Aggregate rows into JSON array
SELECT JSON_ARRAYAGG(name) FROM employees WHERE dept = 'Engineering';
-- Result: ["Animesh", "Rahul", "Sneha"]

-- Aggregate rows into JSON object (key-value)
SELECT JSON_OBJECTAGG(name, salary) FROM employees;
-- Result: {"Animesh": 95000, "Rahul": 72000}
```

---

### JSON Quick Reference

| Function | Does |
|----------|------|
| `JSON_EXTRACT(col, '$.key')` | Extract value by path |
| `col->>'$.key'` | Shorthand extract (unquoted) |
| `JSON_LENGTH(col)` | Length of array or object |
| `JSON_OBJECT(k, v)` | Build JSON object |
| `JSON_ARRAY(a, b)` | Build JSON array |
| `JSON_ARRAYAGG(col)` | Aggregate rows into JSON array |
| `JSON_OBJECTAGG(k, v)` | Aggregate rows into JSON object |

> **Q: How do you index a JSON field?**
> Use a generated/virtual column + index on that column:

```sql
ALTER TABLE events
  ADD COLUMN action VARCHAR(50)
  GENERATED ALWAYS AS (payload->>'$.action') VIRTUAL;

CREATE INDEX idx_action ON events(action);
```

---

## 9. Query Optimization Patterns

> **The #1 topic in senior DE interviews — "how would you speed this up?"**

---

### Pattern 1: Avoid SELECT *

```sql
❌ SELECT * FROM orders;              -- reads all columns, more I/O
✅ SELECT order_id, amount FROM orders; -- only what you need
```

---

### Pattern 2: Predicate Pushdown

```sql
-- Push filters as early (deep) as possible
❌ SELECT * FROM (SELECT * FROM orders) t WHERE t.status = 'Completed';
✅ SELECT * FROM orders WHERE status = 'Completed';  -- filter at source
```

---

### Pattern 3: Partition Pruning

```sql
-- Always filter on partition column
✅ WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31'
❌ WHERE YEAR(order_date) = 2024   -- function on column disables pruning!
```

---

### Pattern 4: Avoid Functions on Indexed Columns in WHERE

```sql
❌ WHERE UPPER(name) = 'ANIMESH'        -- index on name is ignored
✅ WHERE name = 'Animesh'               -- index used

❌ WHERE DATE(created_at) = '2024-01-01'  -- index ignored
✅ WHERE created_at >= '2024-01-01'
     AND created_at <  '2024-01-02'       -- index used ✅
```

---

### Pattern 5: Use EXISTS instead of IN for large subqueries

```sql
❌ WHERE id IN (SELECT customer_id FROM orders WHERE amount > 1000)
   -- evaluates entire subquery, loads all IDs into memory

✅ WHERE EXISTS (SELECT 1 FROM orders o
                 WHERE o.customer_id = c.id AND o.amount > 1000)
   -- stops as soon as first match found
```

---

### Pattern 6: JOIN order matters

```sql
-- Filter early — smaller table first in JOIN chain
✅ FROM small_filtered_table s
   JOIN large_table l ON s.id = l.id
-- reduces rows before the expensive join happens
```

---

### Pattern 7: Covering Index

```sql
-- Query only needs order_id and status
CREATE INDEX idx_covering ON orders(status, order_id);
-- DB never touches main table — all data in the index itself
```

---

### Optimization Quick Checklist

```
Before tuning any slow query, check:
□ Is SELECT * used?           → select only needed columns
□ Is there a WHERE clause?    → add one if missing
□ Is partition column filtered? → check for function wrapping
□ Is there an index?          → EXPLAIN to verify it's used
□ Is IN with large subquery?  → replace with EXISTS
□ Any function on WHERE col?  → remove or rewrite
□ Is DISTINCT overused?       → check if it's really needed
```

---

## 10. AUTO_INCREMENT & Sequences

---

### AUTO_INCREMENT (MySQL)

```sql
CREATE TABLE orders (
  order_id INT PRIMARY KEY AUTO_INCREMENT,
  amount   DECIMAL(10,2)
);

INSERT INTO orders (amount) VALUES (500);   -- order_id auto = 1
INSERT INTO orders (amount) VALUES (1200);  -- order_id auto = 2

-- Check current value
SELECT AUTO_INCREMENT FROM information_schema.TABLES
WHERE TABLE_NAME = 'orders';

-- Reset auto increment
ALTER TABLE orders AUTO_INCREMENT = 1000;

-- Get last inserted ID
SELECT LAST_INSERT_ID();
```

---

### SEQUENCE (PostgreSQL / Oracle)

```sql
-- Create a sequence
CREATE SEQUENCE order_seq START 1000 INCREMENT BY 1;

-- Use in table
CREATE TABLE orders (
  order_id INT DEFAULT NEXTVAL('order_seq'),
  amount   DECIMAL
);

-- Get next value manually
SELECT NEXTVAL('order_seq');   -- 1001
SELECT CURRVAL('order_seq');   -- current value
```

---

### AUTO_INCREMENT vs SEQUENCE

| | AUTO_INCREMENT | SEQUENCE |
|--|---------------|----------|
| DB | MySQL | PostgreSQL, Oracle |
| Scope | Per table | Standalone object, shareable |
| Control | Limited | Full (start, step, cycle, min, max) |
| Use across tables | ❌ No | ✅ Yes |

> **Q: What happens to AUTO_INCREMENT after a ROLLBACK?**
> The counter does NOT roll back — gaps appear in IDs. This is expected and normal.

> **Q: Why do ID gaps happen?**
> Rolled back inserts, deleted rows, or server restarts. Never rely on IDs being consecutive.

---

## 11. Data Quality Checks in SQL

> **Every DE pipeline needs SQL-based data quality validation.**
> Interviewers test this to see if you think beyond just "moving data."

---

### Null Check

```sql
-- Count NULLs in critical columns
SELECT
  COUNT(*) AS total_rows,
  SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
  SUM(CASE WHEN order_date  IS NULL THEN 1 ELSE 0 END) AS null_order_date,
  SUM(CASE WHEN amount      IS NULL THEN 1 ELSE 0 END) AS null_amount
FROM orders;
```

---

### Duplicate Check

```sql
-- Find duplicate primary keys
SELECT order_id, COUNT(*) AS cnt
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;
```

---

### Referential Integrity Check

```sql
-- Orders with no matching customer (orphan records)
SELECT o.order_id
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
```

---

### Range / Freshness Check

```sql
-- Negative amounts (shouldn't exist)
SELECT * FROM orders WHERE amount < 0;

-- Future dates (data loading error)
SELECT * FROM orders WHERE order_date > CURRENT_DATE;

-- Stale data check — last loaded more than 1 day ago
SELECT MAX(order_date) AS last_loaded,
       DATEDIFF(CURRENT_DATE, MAX(order_date)) AS days_stale
FROM orders;
```

---

### Row Count Reconciliation

```sql
-- Compare source vs destination row counts
SELECT 'source' AS layer, COUNT(*) FROM raw_orders
UNION ALL
SELECT 'staging',          COUNT(*) FROM stg_orders
UNION ALL
SELECT 'final',            COUNT(*) FROM fct_orders;
```

---

## 12. Incremental Load Patterns

> **Full load = reload everything every time (slow, expensive).**
> **Incremental load = only load new/changed data (fast, scalable).**

---

### Pattern 1: Timestamp-based Incremental

```sql
-- Load only rows updated since last run
INSERT INTO fct_orders
SELECT * FROM raw_orders
WHERE updated_at > (SELECT MAX(updated_at) FROM fct_orders);
```

---

### Pattern 2: Watermark Table

```sql
-- Store last loaded timestamp
CREATE TABLE pipeline_watermarks (
  table_name  VARCHAR(100),
  last_loaded TIMESTAMP
);

-- Load incrementally
INSERT INTO fct_orders
SELECT * FROM raw_orders
WHERE updated_at > (
  SELECT last_loaded FROM pipeline_watermarks
  WHERE table_name = 'fct_orders'
);

-- Update watermark after load
UPDATE pipeline_watermarks
SET last_loaded = NOW()
WHERE table_name = 'fct_orders';
```

---

### Pattern 3: DELETE + INSERT (for small partitions)

```sql
-- Delete today's data and reload fresh
DELETE FROM fct_orders
WHERE DATE(order_date) = CURRENT_DATE;

INSERT INTO fct_orders
SELECT * FROM raw_orders
WHERE DATE(order_date) = CURRENT_DATE;
```

---

### Pattern 4: UPSERT / MERGE (insert new, update changed)

```sql
INSERT INTO fct_orders (order_id, amount, status, updated_at)
SELECT order_id, amount, status, updated_at FROM raw_orders
ON DUPLICATE KEY UPDATE
  amount     = VALUES(amount),
  status     = VALUES(status),
  updated_at = VALUES(updated_at);
```

---

### Incremental Load Decision Guide

```
Data changes how?             Use pattern:
─────────────────────────────────────────────
Append-only (logs, events)  → Timestamp watermark
Updates happen (CDC)        → UPSERT / MERGE
Small daily partitions      → Delete + Insert
Large historical backfill   → Partition swap
```

> **Q: What is CDC (Change Data Capture)?**
> Tracking every INSERT/UPDATE/DELETE in source DB and streaming those changes
> to target. Tools: Debezium, AWS DMS, Kafka Connect.

---

## 13. Surrogate Keys in Data Warehouses

> **In DWH, you never use the source system's natural key as PK directly.**

```
Source system:  customer_id = 'CUST_101'   (natural key — string, can change)
DWH:            customer_sk = 1, 2, 3...   (surrogate key — integer, never changes)
```

```sql
CREATE TABLE dim_customer (
  customer_sk  INT PRIMARY KEY AUTO_INCREMENT,  -- surrogate key (DWH internal)
  customer_id  VARCHAR(50),                      -- natural/business key (from source)
  name         VARCHAR(100),
  city         VARCHAR(50),
  valid_from   DATE,
  valid_to     DATE,
  is_current   BOOLEAN
);
```

> **Q: Why use surrogate keys in DWH?**
> Natural keys from source systems can change, contain nulls, or be non-numeric (slow joins).
> Surrogate keys are stable integers — fast to join, immune to source system changes.

> **Q: How do you look up surrogate key during ETL load?**
> Lookup join:

```sql
INSERT INTO fct_orders (order_sk, customer_sk, amount)
SELECT
  o.order_id,
  c.customer_sk,         -- lookup from dim table
  o.amount
FROM raw_orders o
JOIN dim_customer c
  ON o.customer_id = c.customer_id
  AND c.is_current = TRUE;
```

---

## 14. Bucketing vs Partitioning

> **Both improve query performance — but work differently.**
> Mostly relevant for Hive, Spark SQL, and big data SQL engines.

```
Partitioning:                    Bucketing:
Split by VALUE of a column       Split by HASH of a column
├── partition=2023               ├── bucket_0 (hash % 4 = 0)
├── partition=2024               ├── bucket_1 (hash % 4 = 1)
└── partition=2025               ├── bucket_2 (hash % 4 = 2)
                                 └── bucket_3 (hash % 4 = 3)
```

| | Partitioning | Bucketing |
|--|-------------|-----------|
| Based on | Column value | Hash of column |
| Number of splits | Dynamic (depends on data) | Fixed (you define N buckets) |
| Best for | Filtering by partition column | JOIN optimization, sampling |
| Skew risk | ✅ Can cause data skew | ❌ More even distribution |
| Used in | Hive, Spark, BigQuery, Redshift | Hive, Spark |

> **Q: When is bucketing better than partitioning?**
> When joining two large tables on the same bucketed column — Spark/Hive can do
> bucket-to-bucket joins, avoiding expensive shuffles.

> **Q: Can you partition AND bucket a table?**
> Yes — partition by date, bucket by user_id for best of both worlds.

```sql
-- Hive example
CREATE TABLE orders (order_id INT, user_id INT, amount DECIMAL)
PARTITIONED BY (order_date STRING)
CLUSTERED BY (user_id) INTO 32 BUCKETS;
```

---

## 15. DE Interview Fire Round ⚡

| Question | Answer |
|----------|--------|
| ETL vs ELT? | ETL transforms before load. ELT loads raw then transforms inside DWH. |
| What is dbt? | SQL-based ELT framework — writes transforms as SELECT models. |
| SCD Type 2 columns? | `valid_from`, `valid_to`, `is_current` |
| FLOAT vs DECIMAL for money? | Always DECIMAL — FLOAT is approximate, causes rounding errors. |
| Why partition pruning fails? | Function wrapping on partition column — `YEAR(date)` instead of range filter. |
| INTERSECT vs INNER JOIN? | INTERSECT compares full rows across two queries. JOIN combines columns. |
| Temp table vs CTE performance? | Temp table materializes once. CTE may re-execute each reference. |
| What is a watermark in pipelines? | Stored timestamp of last successful load — used for incremental extraction. |
| What is CDC? | Change Data Capture — tracks row-level changes (INSERT/UPDATE/DELETE) in source. |
| Why surrogate keys in DWH? | Natural keys change, can be null, or are slow strings. Surrogate = stable integer. |
| Partition vs bucket? | Partition = split by value. Bucket = split by hash. Bucket better for joins. |
| NOT IN with NULLs problem? | If subquery returns NULL, NOT IN returns no rows. Use NOT EXISTS instead. |
| What is predicate pushdown? | Filter data as early as possible, ideally at source/scan layer. |
| JSON_EXTRACT vs ->? | Same thing — `->` is MySQL shorthand for `JSON_EXTRACT`. |
| What causes ID gaps in AUTO_INCREMENT? | Rolled back transactions — counter increments even on rollback. |

---

*⚙️ Data Engineering focused · DE interview complete coverage · Zero overlap with sqltheory.md*
