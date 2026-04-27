# ⚙️ Data Modelling — Practical Patterns & DE Design

> How to actually design · Layers · Modern approaches · Real SQL · DE interview patterns

---

## 📑 Table of Contents

| # | Topic |
|---|-------|
| 1 | [Data Layers — Bronze, Silver, Gold](#1-data-layers--bronze-silver-gold) |
| 2 | [Designing a Data Model — Step by Step](#2-designing-a-data-model--step-by-step) |
| 3 | [Dimension Design Patterns](#3-dimension-design-patterns) |
| 4 | [Fact Table Design Patterns](#4-fact-table-design-patterns) |
| 5 | [Bridge Tables](#5-bridge-tables) |
| 6 | [Aggregate / Summary Tables](#6-aggregate--summary-tables) |
| 7 | [Modern Approaches — Lakehouse & OBT](#7-modern-approaches--lakehouse--obt) |
| 8 | [Incremental Modelling Patterns](#8-incremental-modelling-patterns) |
| 9 | [Data Model Anti-Patterns](#9-data-model-anti-patterns) |
| 10 | [Naming Conventions](#10-naming-conventions) |
| 11 | [DE Interview Design Questions](#11-de-interview-design-questions) |
| 12 | [Advanced DE Fire Round](#12-advanced-de-fire-round-) |

---

## 1. Data Layers — Bronze, Silver, Gold

> **The most common data architecture pattern in modern DE.**
> Also called: Raw / Staging / Serving, or Landing / Cleansed / Curated.

```
SOURCE SYSTEMS
(MySQL, APIs, Kafka, S3 files)
        │
        ▼
┌───────────────────────────────────────────────────────┐
│  BRONZE  (Raw Layer)                                  │
│  • Exact copy of source — no transformation           │
│  • Append-only — nothing ever deleted                 │
│  • Partitioned by ingestion date                      │
│  • Schema: whatever source sends (even messy)         │
│  • Format: JSON, CSV, Parquet as-is                   │
└───────────────────────┬───────────────────────────────┘
                        │ clean & validate
                        ▼
┌───────────────────────────────────────────────────────┐
│  SILVER  (Cleansed Layer)                             │
│  • Cleaned, validated, deduplicated                   │
│  • Standardized data types, column names              │
│  • NULL handling applied                              │
│  • Normalized (still close to source structure)       │
│  • Format: Parquet / Delta Lake                       │
└───────────────────────┬───────────────────────────────┘
                        │ model & aggregate
                        ▼
┌───────────────────────────────────────────────────────┐
│  GOLD  (Serving Layer)                                │
│  • Business-ready, denormalized                       │
│  • Star schema / data marts                           │
│  • Optimized for query performance                    │
│  • What analysts and BI tools query                   │
│  • Format: Parquet / Delta / DWH tables               │
└───────────────────────────────────────────────────────┘
        │
        ▼
CONSUMERS: Dashboards, ML models, Reports, APIs
```

### Layer Naming Conventions

| Layer | Also called | Example tables |
|-------|-------------|----------------|
| Bronze | Raw, Landing, L1 | `raw.orders`, `raw.customers` |
| Silver | Staging, Cleansed, L2 | `stg.orders`, `stg.customers` |
| Gold | Serving, Curated, L3 | `fct_sales`, `dim_customer`, `mart_revenue` |

> **Q: Why keep the Bronze layer untransformed?**
> It's your audit trail and recovery point.
> If a transformation is wrong, you can re-process from Bronze.
> Without it, bad data is gone forever.

> **Q: What transformations happen in Silver?**
> Deduplication, NULL handling, data type casting, column renaming,
> format standardization, PII masking — no business logic yet.

---

## 2. Designing a Data Model — Step by Step

> **Interview scenario: "Design a data model for an e-commerce platform."**
> Here's the exact thought process to walk through:

```
STEP 1: Understand the business process
─────────────────────────────────────────
"What events/transactions are we tracking?"
→ Customer places an order, order ships, customer returns item

STEP 2: Identify grain (most important!)
─────────────────────────────────────────
"What does one row represent?"
→ fact_orders:  one order line item
→ fact_returns: one return event

STEP 3: List dimensions (context)
─────────────────────────────────────────
Who?   → dim_customer
What?  → dim_product
When?  → dim_date
Where? → dim_store / dim_location
How?   → dim_payment_method

STEP 4: List facts (measures)
─────────────────────────────────────────
→ quantity, unit_price, discount, total_amount, shipping_cost

STEP 5: Identify slowly changing dims
─────────────────────────────────────────
→ dim_customer (address can change) → SCD Type 2
→ dim_product  (price can change)   → SCD Type 2

STEP 6: Draw it out
─────────────────────────────────────────
→ Sketch star schema on paper/whiteboard
```

**Resulting model:**

```sql
-- Dimensions
CREATE TABLE dim_customer (
  customer_sk   BIGINT PRIMARY KEY,
  customer_id   VARCHAR(50),          -- natural key
  name          VARCHAR(100),
  email         VARCHAR(100),
  city          VARCHAR(50),
  country       VARCHAR(50),
  segment       VARCHAR(30),          -- 'Premium','Regular','New'
  valid_from    DATE,
  valid_to      DATE DEFAULT '9999-12-31',
  is_current    BOOLEAN DEFAULT TRUE
);

CREATE TABLE dim_product (
  product_sk    BIGINT PRIMARY KEY,
  product_id    VARCHAR(50),
  name          VARCHAR(200),
  category      VARCHAR(100),
  brand         VARCHAR(100),
  cost_price    DECIMAL(10,2),
  valid_from    DATE,
  valid_to      DATE DEFAULT '9999-12-31',
  is_current    BOOLEAN DEFAULT TRUE
);

CREATE TABLE dim_date (
  date_sk       INT PRIMARY KEY,      -- e.g. 20240317
  full_date     DATE,
  year          INT,
  quarter       INT,
  month         INT,
  month_name    VARCHAR(10),
  week          INT,
  day_of_week   INT,
  day_name      VARCHAR(10),
  is_weekend    BOOLEAN,
  is_holiday    BOOLEAN
);

-- Fact table
CREATE TABLE fact_order_lines (
  order_line_sk     BIGINT PRIMARY KEY,
  order_id          VARCHAR(50),          -- degenerate dim
  customer_sk       BIGINT REFERENCES dim_customer(customer_sk),
  product_sk        BIGINT REFERENCES dim_product(product_sk),
  order_date_sk     INT    REFERENCES dim_date(date_sk),
  ship_date_sk      INT    REFERENCES dim_date(date_sk),   -- role-playing
  quantity          INT,
  unit_price        DECIMAL(10,2),
  discount_pct      DECIMAL(5,2),
  total_amount      DECIMAL(10,2),
  shipping_cost     DECIMAL(10,2)
);
```

---

## 3. Dimension Design Patterns

### Pattern 1: dim_date — Always pre-built

```sql
-- Generate dim_date (pre-populate for 10 years)
-- 1 row per day — never changes — no SCD needed
INSERT INTO dim_date
SELECT
  CAST(DATE_FORMAT(d, '%Y%m%d') AS INT)  AS date_sk,
  d                                       AS full_date,
  YEAR(d)                                 AS year,
  QUARTER(d)                              AS quarter,
  MONTH(d)                                AS month,
  MONTHNAME(d)                            AS month_name,
  WEEK(d)                                 AS week,
  DAYOFWEEK(d)                            AS day_of_week,
  DAYNAME(d)                              AS day_name,
  CASE WHEN DAYOFWEEK(d) IN (1,7)
       THEN TRUE ELSE FALSE END           AS is_weekend
FROM (
  -- generate date series
  SELECT DATE_ADD('2020-01-01', INTERVAL seq DAY) AS d
  FROM seq_0_to_3650   -- 10 years
) dates;
```

> **Why pre-build dim_date instead of using date functions?**
> Pre-built = instant lookup (no computation per query).
> Can add custom columns: `is_fiscal_quarter`, `is_holiday`, `season`.
> Analysts filter by `WHERE d.month_name = 'January'` — much cleaner.

---

### Pattern 2: Junk Dimension

```
Problem: fact table has many small flag columns
  fact_orders: is_promotional, is_online, is_gift_wrapped,
               payment_is_cod, is_first_order → 5 extra columns

Solution: combine into one junk dimension
  dim_order_type: all combinations of flags as rows
```

```sql
CREATE TABLE dim_order_type (
  order_type_sk   INT PRIMARY KEY,
  is_promotional  BOOLEAN,
  is_online       BOOLEAN,
  is_gift_wrapped BOOLEAN,
  is_cod          BOOLEAN,
  is_first_order  BOOLEAN
);

-- Pre-populate all combinations (2^5 = 32 rows max)
INSERT INTO dim_order_type VALUES
(1, FALSE, FALSE, FALSE, FALSE, FALSE),
(2, TRUE,  FALSE, FALSE, FALSE, FALSE),
(3, FALSE, TRUE,  FALSE, FALSE, FALSE),
-- ... all 32 combinations

-- fact table just stores one FK
fact_orders.order_type_sk → dim_order_type
```

---

### Pattern 3: Role-Playing Dimensions

```sql
-- Same dim_date used 3 ways in one fact table
SELECT
  o.order_id,
  od.full_date  AS order_date,
  sd.full_date  AS ship_date,
  dd.full_date  AS delivery_date,
  o.total_amount
FROM fact_orders o
JOIN dim_date od ON o.order_date_sk  = od.date_sk   -- role 1
JOIN dim_date sd ON o.ship_date_sk   = sd.date_sk   -- role 2
JOIN dim_date dd ON o.delivery_date_sk = dd.date_sk -- role 3
```

---

## 4. Fact Table Design Patterns

### Pattern 1: Transaction Fact Table

```
One row per atomic transaction event.
Most common type.

fact_sales: one row = one line item sold
fact_payments: one row = one payment
fact_clicks: one row = one click event
```

### Pattern 2: Periodic Snapshot Fact Table

```
One row per entity per time period — regardless of activity.
Captures state at regular intervals.

fact_inventory_daily:
  date_sk | product_sk | store_sk | stock_on_hand | reorder_point
  (captured every day, even if no change)

USE WHEN: Need to track status over time (inventory, account balance)
```

```sql
-- Load daily inventory snapshot
INSERT INTO fact_inventory_daily
SELECT
  20240317          AS date_sk,
  product_id        AS product_sk,
  store_id          AS store_sk,
  current_stock     AS stock_on_hand,
  reorder_level     AS reorder_point
FROM inventory_current;
-- Runs every day — creates full history of inventory levels
```

### Pattern 3: Accumulating Snapshot Fact Table

```
One row per process instance — updated as process moves through stages.
Tracks pipeline/workflow progress.

fact_order_fulfillment:
  order_sk | ordered_date_sk | picked_date_sk | shipped_date_sk | delivered_date_sk
  (one row per order, dates filled in as stages complete)
```

```sql
CREATE TABLE fact_order_fulfillment (
  order_sk           BIGINT PRIMARY KEY,
  customer_sk        BIGINT,
  ordered_date_sk    INT,
  picked_date_sk     INT,     -- NULL until picked
  shipped_date_sk    INT,     -- NULL until shipped
  delivered_date_sk  INT,     -- NULL until delivered
  days_to_ship       INT,     -- calculated when shipped
  days_to_deliver    INT      -- calculated when delivered
);
-- Updated (not inserted) when each stage completes
```

### Three Fact Table Types Summary

| Type | Grain | Updated? | Use case |
|------|-------|----------|----------|
| **Transaction** | One event | ❌ Never (append-only) | Sales, clicks, payments |
| **Periodic Snapshot** | Entity per period | ❌ Append daily | Inventory, balances |
| **Accumulating Snapshot** | One process instance | ✅ Updated at each stage | Order fulfillment, pipelines |

---

## 5. Bridge Tables

> **Handle many-to-many relationships between fact and dimension.**

```
Problem: One order can have multiple promotions
         One promotion can apply to many orders
         → many-to-many → can't put in fact directly

Solution: Bridge table
```

```
fact_orders ──► bridge_order_promotion ◄── dim_promotion
```

```sql
CREATE TABLE dim_promotion (
  promotion_sk   INT PRIMARY KEY,
  promotion_id   VARCHAR(50),
  name           VARCHAR(100),
  discount_type  VARCHAR(30),
  discount_value DECIMAL(10,2)
);

CREATE TABLE bridge_order_promotion (
  order_sk       BIGINT,
  promotion_sk   INT,
  weighting_factor DECIMAL(5,4),  -- allocate credit across promos
  PRIMARY KEY (order_sk, promotion_sk)
);

-- Query: orders with their promotions
SELECT o.order_id, p.name AS promotion
FROM fact_orders o
JOIN bridge_order_promotion b ON o.order_sk = b.order_sk
JOIN dim_promotion p ON b.promotion_sk = p.promotion_sk;
```

> **Q: When do you use a bridge table?**
> When a fact row has a multi-valued dimension (multiple tags, multiple promotions, multiple categories).

---

## 6. Aggregate / Summary Tables

> **Pre-computed summaries for faster dashboard queries.**

```
Without aggregate table:
SELECT region, SUM(amount) FROM fact_sales        -- scans 1 billion rows
JOIN dim_customer ON ...
JOIN dim_date ON ...
WHERE year = 2024
GROUP BY region;  → 30 seconds 😰

With aggregate table (pre-computed daily):
SELECT region, SUM(daily_revenue) FROM agg_sales_daily  -- scans 365 rows
WHERE year = 2024
GROUP BY region;  → 0.1 seconds ✅
```

```sql
-- Build aggregate table (runs daily via Airflow)
CREATE TABLE agg_daily_sales_by_region AS
SELECT
  d.full_date,
  d.year,
  d.month,
  c.country,
  c.city            AS region,
  COUNT(*)          AS order_count,
  SUM(f.quantity)   AS total_quantity,
  SUM(f.total_amount) AS daily_revenue,
  AVG(f.total_amount) AS avg_order_value
FROM fact_order_lines f
JOIN dim_date     d ON f.order_date_sk = d.date_sk
JOIN dim_customer c ON f.customer_sk   = c.customer_sk
  AND c.is_current = TRUE
GROUP BY d.full_date, d.year, d.month, c.country, c.city;
```

> **Q: Aggregate table vs Materialized View?**
> Aggregate table = regular table, refreshed by ETL job, full control.
> Materialized View = DB-managed, refreshed on schedule or on demand.
> For DWH, aggregate tables are more common (ETL controls refresh timing).

---

## 7. Modern Approaches — Lakehouse & OBT

### The Lakehouse Architecture

```
Traditional:                    Modern Lakehouse:
OLTP DB                         OLTP DB
   ↓ ETL                           ↓ CDC / batch
Data Warehouse                  Data Lake (S3/GCS)
(expensive, rigid)              ├── Bronze (raw)
   ↓                            ├── Silver (clean)
BI Tool                         └── Gold (served)
                                       ↓
                                Delta Lake / Iceberg
                                (ACID on object storage)
                                       ↓
                                Query Engine (Spark SQL,
                                Trino, DuckDB, Athena)
                                       ↓
                                BI Tool / ML / API
```

**Key lakehouse technologies:**

| Layer | Technology |
|-------|-----------|
| Storage | S3, GCS, ADLS |
| Table format | Delta Lake, Apache Iceberg, Apache Hudi |
| Query engine | Spark SQL, Trino, DuckDB, Athena, BigQuery |
| Orchestration | Airflow, dbt |
| Serving | Redshift, BigQuery, Snowflake |

---

### One Big Table (OBT)

> **Modern alternative to star schema — one wide denormalized table.**

```
Star Schema:                      One Big Table (OBT):
fact_sales                        sales_obt
+ JOIN dim_customer               ├── order_id
+ JOIN dim_product        →       ├── customer_name
+ JOIN dim_date                   ├── customer_city
= 4 table query                   ├── product_name
                                  ├── product_category
                                  ├── order_date
                                  ├── year, month, quarter
                                  ├── quantity
                                  └── total_amount
```

```sql
-- Build OBT
CREATE TABLE sales_obt AS
SELECT
  f.order_id,
  f.quantity,
  f.total_amount,
  c.name          AS customer_name,
  c.city          AS customer_city,
  c.segment       AS customer_segment,
  p.name          AS product_name,
  p.category      AS product_category,
  p.brand         AS product_brand,
  d.full_date     AS order_date,
  d.year,
  d.month,
  d.quarter,
  d.is_weekend
FROM fact_order_lines f
JOIN dim_customer c ON f.customer_sk   = c.customer_sk AND c.is_current = TRUE
JOIN dim_product  p ON f.product_sk    = p.product_sk  AND p.is_current = TRUE
JOIN dim_date     d ON f.order_date_sk = d.date_sk;
```

| | Star Schema | One Big Table |
|--|-------------|---------------|
| Query complexity | JOINs needed | Single table scan |
| Storage | Less (no duplication) | More (duplicated dims) |
| Flexibility | High (mix dims freely) | Lower (fixed columns) |
| Performance | Good | ✅ Fastest for columnar |
| Best for | Complex analytics | Simple dashboards, ML features |

> **Q: When would you choose OBT over star schema?**
> When the primary use case is simple reporting or ML feature stores.
> Columnar engines (BigQuery, Redshift) are very efficient on wide tables.
> dbt often builds OBTs as the final mart layer.

---

## 8. Incremental Modelling Patterns

> **Full refresh every run is expensive — incremental is the production standard.**

### Pattern 1: Insert new rows only (append-only facts)

```sql
-- Load only today's new transactions
INSERT INTO fact_order_lines
SELECT * FROM stg_order_lines
WHERE order_date = CURRENT_DATE;
-- Never update, never delete — transaction facts are immutable
```

### Pattern 2: Upsert (insert new + update changed)

```sql
-- Merge new/changed records
INSERT INTO dim_customer
  (customer_id, name, city, valid_from, valid_to, is_current)
SELECT
  s.customer_id,
  s.name,
  s.city,
  CURRENT_DATE,
  '9999-12-31',
  TRUE
FROM stg_customers s
LEFT JOIN dim_customer d
  ON s.customer_id = d.customer_id AND d.is_current = TRUE
WHERE d.customer_id IS NULL               -- new customers
   OR s.city != d.city                   -- changed city
   OR s.name != d.name;                  -- changed name
```

### Pattern 3: Partition overwrite

```sql
-- Delete and reload one partition (today's data)
DELETE FROM fact_order_lines WHERE order_date = CURRENT_DATE;
INSERT INTO fact_order_lines SELECT * FROM stg_order_lines
WHERE order_date = CURRENT_DATE;
-- Idempotent — safe to re-run ✅
```

### Pattern 4: Watermark-based incremental

```sql
-- Load only rows newer than last successful load
INSERT INTO fact_events
SELECT * FROM raw_events
WHERE created_at > (SELECT MAX(created_at) FROM fact_events);
```

### Idempotency — Critical Concept

```
Idempotent = running the pipeline multiple times gives the same result.

❌ NOT idempotent:
INSERT INTO fact_sales SELECT * FROM stg_sales;
→ run twice = duplicate rows!

✅ Idempotent:
DELETE FROM fact_sales WHERE date = CURRENT_DATE;
INSERT INTO fact_sales SELECT * FROM stg_sales WHERE date = CURRENT_DATE;
→ run twice = same result ✅
```

> **Q: Why is idempotency important in data pipelines?**
> Pipelines fail and need to be re-run. If re-running creates duplicates or
> wrong data, your DWH becomes unreliable. Idempotent pipelines can safely
> be retried without side effects.

---

## 9. Data Model Anti-Patterns

> **What NOT to do — and how to fix it.**

---

### ❌ Anti-pattern 1: Entity-Attribute-Value (EAV)

```sql
-- EAV: flexible but terrible for analytics
CREATE TABLE product_attributes (
  product_id  INT,
  attr_name   VARCHAR(100),
  attr_value  VARCHAR(500)
);
-- Data:
-- 1 | color    | red
-- 1 | size     | large
-- 1 | weight   | 2.5kg

-- To query: SELECT color, size → 2 self-joins needed 😰
-- Analytics on this = nightmare
```

```sql
-- ✅ Fix: proper columns
CREATE TABLE dim_product (
  product_sk  BIGINT PRIMARY KEY,
  color       VARCHAR(50),
  size        VARCHAR(20),
  weight_kg   DECIMAL(5,2)
);
```

---

### ❌ Anti-pattern 2: Storing calculated metrics in fact table

```sql
-- ❌ BAD: pre-calculated column
CREATE TABLE fact_sales (
  amount       DECIMAL,
  discount     DECIMAL,
  tax          DECIMAL,
  total        DECIMAL,       -- amount - discount + tax
  profit_margin DECIMAL       -- (amount - cost) / amount
);
-- Problem: if formula changes, must recalculate all historical data

-- ✅ FIX: store atomic facts, calculate in query or view
CREATE TABLE fact_sales (
  amount       DECIMAL,
  discount     DECIMAL,
  tax          DECIMAL,
  cost         DECIMAL
  -- total = amount - discount + tax (compute in query)
);
```

---

### ❌ Anti-pattern 3: Mixed grain in fact table

```sql
-- ❌ BAD: some rows are line items, some are order totals
fact_orders:
  row 1: order_id=1, product_id=A, amount=100  (line item)
  row 2: order_id=1, product_id=NULL, amount=180 (order total)
  → SUM(amount) = 280 (WRONG — double counted!)

-- ✅ FIX: separate tables for each grain
fact_order_lines  (one row = one line item)
fact_orders       (one row = one order total)
```

---

### ❌ Anti-pattern 4: NULL foreign keys in fact table

```sql
-- ❌ BAD: NULL customer_sk — breaks JOINs
INSERT INTO fact_sales (customer_sk, amount) VALUES (NULL, 500);

-- ✅ FIX: use "unknown" member row
INSERT INTO dim_customer VALUES (-1, 'UNKNOWN', 'Unknown', ...);
INSERT INTO fact_sales (customer_sk, amount) VALUES (-1, 500);
-- Joins work! -1 → "Unknown" row in dim
```

---

### ❌ Anti-pattern 5: Using source natural keys as DWH primary keys

```sql
-- ❌ BAD: using source customer_id as PK in DWH
CREATE TABLE dim_customer (
  customer_id VARCHAR(50) PRIMARY KEY,  -- source key as PK
  ...
);
-- Problem: source can change this key. SCD Type 2 impossible.

-- ✅ FIX: surrogate key
CREATE TABLE dim_customer (
  customer_sk  BIGINT PRIMARY KEY AUTO_INCREMENT,  -- surrogate
  customer_id  VARCHAR(50),                          -- natural key (kept for reference)
  ...
);
```

---

## 10. Naming Conventions

> **Consistent naming = self-documenting model. Interviewers notice this.**

```
Tables:
  fact_*           → fact tables          (fact_sales, fact_returns)
  dim_*            → dimension tables     (dim_customer, dim_date)
  stg_*            → staging tables       (stg_orders, stg_customers)
  raw_*            → raw/bronze tables    (raw_orders)
  agg_*            → aggregate tables     (agg_daily_revenue)
  bridge_*         → bridge tables        (bridge_order_promo)
  mart_*           → data mart tables     (mart_sales_summary)

Columns:
  *_sk             → surrogate key        (customer_sk)
  *_id             → natural/business key (customer_id)
  *_date           → date column          (order_date)
  *_sk (FK)        → foreign key          (product_sk in fact)
  is_*             → boolean flag         (is_current, is_active)
  *_at             → timestamp            (created_at, updated_at)
  valid_from/to    → SCD Type 2 dates
  *_count          → count metric         (order_count)
  *_amount         → money metric         (total_amount)

General rules:
  ✅ snake_case (not camelCase or PascalCase)
  ✅ lowercase always
  ✅ descriptive but not overly long
  ✅ consistent across all tables
  ❌ abbreviations (use 'customer' not 'cust')
  ❌ spaces or special characters
  ❌ reserved words (date, order, group)
```

---

## 11. DE Interview Design Questions

> **Common "design a model for X" interview questions with approaches.**

---

### Q: Design a data model for Uber/Ola

```
Business processes: trips, payments, driver ratings

Grain: one trip

Dimensions:
  dim_driver    (driver_sk, name, rating, vehicle_type)
  dim_passenger (passenger_sk, name, segment)
  dim_date      (date_sk, ...)
  dim_location  (location_sk, city, zone, lat, lng)

Fact:
  fact_trips:
    trip_sk, driver_sk, passenger_sk,
    request_date_sk, complete_date_sk,
    pickup_location_sk, dropoff_location_sk,
    distance_km, duration_mins,
    base_fare, surge_multiplier, total_fare,
    driver_rating, passenger_rating
```

---

### Q: Design a model for an e-learning platform

```
Business processes: course enrollments, lesson completions, quiz attempts

Grain (fact_enrollments): one enrollment (student + course)
Grain (fact_lesson_progress): one lesson completion

Dimensions:
  dim_student  (student_sk, name, subscription_type, country)
  dim_course   (course_sk, title, category, instructor_sk, level)
  dim_lesson   (lesson_sk, title, type, duration_mins, course_sk)
  dim_date     (date_sk, ...)

Facts:
  fact_enrollments:
    enrollment_sk, student_sk, course_sk,
    enroll_date_sk, complete_date_sk,
    progress_pct, is_completed, certificate_issued

  fact_lesson_completions:
    completion_sk, student_sk, lesson_sk, course_sk,
    completion_date_sk, time_spent_mins, attempts
```

---

### Q: Design a model for a food delivery app (Swiggy/Zomato)

```
Grain: one order line item

Dimensions:
  dim_customer   (customer_sk, name, city, loyalty_tier)
  dim_restaurant (restaurant_sk, name, cuisine, city, rating)
  dim_menu_item  (item_sk, name, category, is_veg, restaurant_sk)
  dim_date       (date_sk, ...)
  dim_delivery_zone (zone_sk, city, zone_name)

Fact:
  fact_order_items:
    order_item_sk, order_id (degenerate),
    customer_sk, restaurant_sk, item_sk,
    order_date_sk, delivery_zone_sk,
    quantity, item_price, discount,
    total_amount, delivery_fee,
    prep_time_mins, delivery_time_mins,
    customer_rating, is_reorder
```

---

## 12. Advanced DE Fire Round ⚡

> **Q: What is the medallion architecture?**
> Bronze (raw) → Silver (cleaned) → Gold (served). Three-layer pattern for
> organizing data in a lakehouse. Each layer adds more quality and structure.

> **Q: What is idempotency and why does it matter?**
> Pipeline that produces same result regardless of how many times it runs.
> Critical for retry safety — failed pipelines get re-run; must not create duplicates.

> **Q: What is the difference between a transaction fact and a periodic snapshot fact?**
> Transaction = one row per event, append-only (sales, clicks).
> Periodic snapshot = one row per entity per period, captures state (inventory levels daily).

> **Q: What is an accumulating snapshot fact table?**
> One row per process instance, updated as stages complete.
> e.g. one row per order updated when picked, shipped, delivered.

> **Q: What is a bridge table?**
> Handles many-to-many between fact and dimension.
> e.g. one order → multiple promotions → bridge_order_promotion.

> **Q: What is a junk dimension?**
> Groups low-cardinality flag columns into one dimension to avoid cluttering the fact table.

> **Q: What is OBT (One Big Table)?**
> Fully denormalized single table joining fact + all dims. Fastest for columnar scans,
> simpler for analysts. Trade-off: more storage, less flexibility.

> **Q: Why pre-build dim_date instead of using date functions?**
> Instant lookup, no computation, customizable (fiscal calendar, holidays, seasons).

> **Q: What is a conformed dimension?**
> Shared across multiple fact tables with the same definition.
> Enables cross-process analysis. `dim_date` and `dim_customer` are always conformed.

> **Q: What does "grain" mean and why is it the first thing to define?**
> Grain = what one row represents. Everything else (dims, facts, aggregations) depends on it.
> Wrong grain = wrong numbers that can't be trusted.

> **Q: Kimball vs Inmon?**
> Kimball = bottom-up, star schema, business-first, most common in practice.
> Inmon = top-down, 3NF enterprise DWH first, then data marts.

> **Q: What is a slowly changing fact?**
> A fact that changes slowly over time (unit cost, exchange rate).
> Handled by storing effective dates on the fact or keeping a separate rate table.

---

*⚙️ Data Modelling Patterns · Practical DE design · Interview-ready*
