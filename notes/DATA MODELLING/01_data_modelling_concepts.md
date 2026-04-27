# 🗄️ Data Modelling — Core Concepts

> 0–2 yr DE level · Theory-first · Interview-ready · No overkill

---

## 📑 Table of Contents

| # | Topic |
|---|-------|
| 1 | [What is Data Modelling?](#1-what-is-data-modelling) |
| 2 | [Types of Data Models](#2-types-of-data-models) |
| 3 | [Schema Design — Star, Snowflake, Galaxy](#3-schema-design) |
| 4 | [Facts vs Dimensions](#4-facts-vs-dimensions) |
| 5 | [Keys — Natural, Surrogate, Composite](#5-keys) |
| 6 | [Normalization — 1NF to BCNF (DE lens)](#6-normalization--de-lens) |
| 7 | [Dimensional Modelling — Kimball Basics](#7-dimensional-modelling--kimball) |
| 8 | [Slowly Changing Dimensions — SCD](#8-slowly-changing-dimensions-scd) |
| 9 | [Data Vault — Just Enough](#9-data-vault--just-enough) |
| 10 | [OLTP vs OLAP — Modelling Perspective](#10-oltp-vs-olap--modelling-perspective) |
| 11 | [Grain — The Most Important Concept](#11-grain--the-most-important-concept) |
| 12 | [Interview Q&A Fire Round](#12-interview-qa-fire-round-) |

---

## 1. What is Data Modelling?

```
Raw data (messy, unstructured)
        ↓
  Data Modelling
  "How should we organize and
   structure data so it's useful,
   queryable, and trustworthy?"
        ↓
Structured tables with relationships,
rules, and clear meaning
```

> **Data modelling** is the process of designing how data is stored, organised,
> and related — so that queries are fast, data is consistent, and business
> questions can actually be answered.

**Why it matters for a DE:**
- You design the tables that analysts/scientists query daily
- Bad models = slow queries, wrong numbers, confused users
- Good models = fast dashboards, trustworthy metrics, happy stakeholders

```
Without modelling:             With modelling:
┌────────────────────┐         ┌──────────────┐   ┌──────────────┐
│ one giant messy    │         │  dim_customer │   │  dim_product │
│ table with 200     │   VS    └──────┬───────┘   └──────┬───────┘
│ columns, NULLs     │                └──────► fact_sales ◄───────┘
│ everywhere 😰      │                         (clean, fast, clear)
└────────────────────┘
```

---

## 2. Types of Data Models

```
Three levels — like zooming in on a blueprint:

Conceptual  →  "What" (business view, no tech detail)
Logical     →  "How" (entities, attributes, relationships — no DB specifics)
Physical    →  "Exact" (actual table/column names, data types, indexes)
```

| Level | Audience | Contains | Example |
|-------|----------|----------|---------|
| **Conceptual** | Business stakeholders | Entities + relationships | Customer places Order |
| **Logical** | Architects / analysts | Tables, columns, keys (no types) | customer(id, name, city) |
| **Physical** | Engineers / DBAs | Actual DDL, data types, partitions | `customer_id BIGINT PK` |

```
Conceptual:              Logical:                Physical (SQL):
[Customer]               customer                CREATE TABLE dim_customer (
    │                      - id                    customer_sk  BIGINT PK,
  places                   - name                  customer_id  VARCHAR(50),
    │                      - city       →           name         VARCHAR(100),
  [Order]                order                     city         VARCHAR(50),
                           - id                    valid_from   DATE,
                           - date                  is_current   BOOLEAN
                           - amount              );
```

---

## 3. Schema Design

### ⭐ Star Schema

```
                     dim_date
                    ┌─────────┐
                    │date_sk  │
                    │year     │
                    │month    │
                    │quarter  │
                    └────┬────┘
                         │
dim_customer        fact_sales          dim_product
┌───────────┐      ┌────────────┐      ┌───────────┐
│customer_sk├─────►│customer_sk │◄─────┤product_sk │
│name       │      │product_sk  │      │name       │
│city       │      │date_sk     │      │category   │
│segment    │      │store_sk    │      │brand      │
└───────────┘      │amount      │      └───────────┘
                   │quantity    │
                   │discount    │      dim_store
                   └────────────┘      ┌───────────┐
                         │◄────────────┤store_sk   │
                                       │city       │
                                       │region     │
                                       └───────────┘
```

- **Fact table** at center — measurable numbers (amount, qty)
- **Dimension tables** around it — descriptive context (who, what, when, where)
- Denormalized — few JOINs, fast queries
- **Best for:** BI dashboards, analytics, reporting

---

### ❄️ Snowflake Schema

```
dim_product ──► dim_category ──► dim_department
    │
dim_brand

(dimensions are further normalized into sub-dimensions)
```

- Dimensions split into sub-tables (normalized)
- More JOINs, saves storage, harder to query
- **Best for:** large DWH where storage matters, strict normalization needed

---

### 🌌 Galaxy Schema (Fact Constellation)

```
dim_customer ──► fact_sales ◄── dim_product
                    │
dim_customer ──► fact_returns ◄── dim_product
                    │
                dim_reason
```

- Multiple fact tables sharing dimension tables
- Complex but powerful for multi-process analytics
- **Best for:** enterprise DWH with multiple business processes

---

### Schema Comparison

| | Star | Snowflake | Galaxy |
|--|------|-----------|--------|
| JOINs needed | Few ✅ | Many | Many |
| Query speed | Fastest ✅ | Slower | Slowest |
| Storage | More | Less ✅ | Depends |
| Complexity | Simple ✅ | Medium | Complex |
| Best for | BI/Dashboards | Large DWH | Enterprise |

> **Q: Which schema is most common in interviews?**
> Star schema — it's the default for most DWH and BI implementations.

---

## 4. Facts vs Dimensions

```
Think of a sales transaction:

WHO bought?   → dim_customer   (dimension)
WHAT?         → dim_product    (dimension)
WHEN?         → dim_date       (dimension)
WHERE?        → dim_store      (dimension)
HOW MUCH?     → fact_sales.amount    (fact — the number)
HOW MANY?     → fact_sales.quantity  (fact — the number)
```

---

### Fact Tables

> Store **measurable, numeric events** — what happened and the numbers around it.

```sql
-- fact table: one row per transaction
CREATE TABLE fact_sales (
  sale_sk      BIGINT PRIMARY KEY,   -- surrogate key
  customer_sk  BIGINT,               -- FK to dim_customer
  product_sk   BIGINT,               -- FK to dim_product
  date_sk      INT,                  -- FK to dim_date
  store_sk     INT,                  -- FK to dim_store
  -- MEASURES (the actual facts):
  quantity     INT,
  unit_price   DECIMAL(10,2),
  discount     DECIMAL(5,2),
  total_amount DECIMAL(10,2)
);
```

**Types of Facts:**

| Type | Description | Example |
|------|-------------|---------|
| **Additive** | Can SUM across ALL dimensions | `sales_amount` |
| **Semi-additive** | Can SUM across SOME dimensions | `account_balance` (not time) |
| **Non-additive** | Cannot SUM meaningfully | `ratio`, `percentage`, `temperature` |

```
Additive:      SUM(sales_amount) by region ✅  by date ✅  by product ✅
Semi-additive: SUM(balance) by customer ✅  but AVG by date (not SUM!) ⚠️
Non-additive:  AVG(ratio) — never SUM a percentage ❌
```

---

### Dimension Tables

> Store **descriptive context** — the "who, what, when, where" of facts.

```sql
CREATE TABLE dim_customer (
  customer_sk  BIGINT PRIMARY KEY,   -- surrogate key (DWH internal)
  customer_id  VARCHAR(50),          -- natural key (from source system)
  name         VARCHAR(100),
  email        VARCHAR(100),
  city         VARCHAR(50),
  country      VARCHAR(50),
  segment      VARCHAR(30),          -- 'Premium', 'Regular', 'New'
  valid_from   DATE,                 -- SCD Type 2
  valid_to     DATE,
  is_current   BOOLEAN
);
```

**Types of Dimensions:**

| Type | Description | Example |
|------|-------------|---------|
| **Conformed** | Shared across multiple fact tables | `dim_date`, `dim_customer` |
| **Degenerate** | No separate table — key lives in fact | `order_id` in fact_sales |
| **Junk** | Miscellaneous low-cardinality flags grouped together | `is_promo`, `is_online`, `is_gift` |
| **Role-playing** | Same dim used multiple times with different aliases | `dim_date` as order_date, ship_date |
| **Slowly Changing** | Dimension that changes over time | customer address, product price |

```
Role-playing dimension example:
fact_orders
  ├── order_date_sk  → dim_date (aliased as "Order Date")
  ├── ship_date_sk   → dim_date (aliased as "Ship Date")
  └── deliver_date_sk→ dim_date (aliased as "Delivery Date")
Same dim_date table, 3 different roles.
```

---

## 5. Keys

```
Source system has: customer_id = 'CUST_101_IN'  ← natural key
DWH assigns:       customer_sk = 1               ← surrogate key
Composite key:     (order_id, product_id)        ← two columns together = unique
```

| Key Type | Description | Lives in |
|----------|-------------|----------|
| **Natural Key** | Business identifier from source system | Source + staging |
| **Surrogate Key** | Auto-generated integer, DWH internal | DWH dims + facts |
| **Composite Key** | Multiple columns together = unique | Bridge tables, facts |
| **Primary Key** | Uniquely identifies a row | Every table |
| **Foreign Key** | Links to another table's PK | Fact tables |

**Why surrogate keys in DWH?**

```
Problem with natural keys:
  customer_id = 'CUST_101'  → can change in source system
  customer_id = NULL         → possible in source
  customer_id = 'C101-IN'   → string = slow JOINs

Surrogate key solution:
  customer_sk = 1            → never changes
  customer_sk = NOT NULL     → always exists
  customer_sk = BIGINT       → fast integer JOINs ✅
```

> **Q: What is an unknown member / default dimension row?**
> A special row in dim tables (surrogate key = -1 or 0) for when FK is unknown/null.
> Instead of NULL FK in fact → use -1 pointing to "Unknown" row.

```sql
INSERT INTO dim_customer VALUES (-1, 'N/A', 'Unknown', 'Unknown', ...);
-- fact_sales.customer_sk = -1 means "customer unknown"
-- avoids NULLs in fact table FKs ✅
```

---

## 6. Normalization — DE Lens

> You already know 1NF–BCNF theory. Here's how a DE **thinks** about it:

```
OLTP (transactional):    Normalize heavily → 3NF
                         Avoids redundancy, fast writes

DWH (analytical):        Denormalize intentionally → Star schema
                         Fewer JOINs, fast reads

Lakehouse (modern):      Raw = normalized staging
                         Curated = denormalized serving layer
```

**The DE rule of thumb:**

```
Closer to source?   → More normalized   (staging layer)
Closer to analyst?  → More denormalized (serving/mart layer)

raw_orders (normalized)
    ↓  ETL
stg_orders (cleaned, still normalized)
    ↓  Transform
fct_orders + dim_* (denormalized star schema)
    ↓  Serve
dashboard / report (analyst queries star schema)
```

> **Q: Should a data warehouse be in 3NF?**
> No — DWH is intentionally denormalized (star/snowflake) for query performance.
> 3NF is for OLTP systems. Kimball's dimensional modelling is the standard for DWH.

---

## 7. Dimensional Modelling — Kimball

> **Ralph Kimball's approach — the dominant DWH design methodology.**
> "Design for the business user, not the database administrator."

### The 4-Step Kimball Design Process

```
Step 1: SELECT THE BUSINESS PROCESS
        "What are we modelling?" → Sales, Returns, Inventory, HR

Step 2: DECLARE THE GRAIN
        "What does one row represent?" → One line item on one invoice

Step 3: IDENTIFY DIMENSIONS
        "What context describes each row?" → Customer, Product, Date, Store

Step 4: IDENTIFY FACTS
        "What numbers do we measure?" → quantity, amount, discount
```

**Example walkthrough — e-commerce sales:**

```
Step 1: Business process  → Online order fulfilment
Step 2: Grain             → One order line item
Step 3: Dimensions        → dim_customer, dim_product, dim_date, dim_payment_method
Step 4: Facts             → quantity, unit_price, discount, total_amount, shipping_cost
```

```sql
-- Resulting fact table (one row = one line item)
CREATE TABLE fact_order_lines (
  order_line_sk      BIGINT PRIMARY KEY,
  order_id           VARCHAR(50),        -- degenerate dim
  customer_sk        BIGINT,
  product_sk         BIGINT,
  order_date_sk      INT,
  payment_method_sk  INT,
  quantity           INT,
  unit_price         DECIMAL(10,2),
  discount_pct       DECIMAL(5,2),
  total_amount       DECIMAL(10,2),
  shipping_cost      DECIMAL(10,2)
);
```

### Conformed Dimensions

```
fact_sales ──────────────────────────────────┐
                                             │
fact_returns ────────────────────────────────┤ shared dim_customer
                                             │
fact_customer_service ───────────────────────┘
```

> A **conformed dimension** is one that is shared across multiple fact tables with the same meaning.
> `dim_date`, `dim_customer`, `dim_product` are almost always conformed.
> This allows cross-process analysis: "How do returns correlate with customer segment?"

---

## 8. Slowly Changing Dimensions (SCD)

> **What do you do when dimension data changes?**
> e.g. Customer moves city, product changes category, employee changes department.

---

### SCD Type 1 — Overwrite

```
Before:  customer_sk=1 | Animesh | Delhi
Change:  Animesh moves to Mumbai
After:   customer_sk=1 | Animesh | Mumbai   ← Delhi gone forever

USE WHEN: History doesn't matter (typos, corrections)
```

```sql
UPDATE dim_customer SET city = 'Mumbai' WHERE customer_sk = 1;
```

---

### SCD Type 2 — New Row ✅ Most common

```
Before:
sk | name    | city   | valid_from | valid_to   | is_current
1  | Animesh | Delhi  | 2020-01-01 | 9999-12-31 | TRUE

After change:
sk | name    | city   | valid_from | valid_to   | is_current
1  | Animesh | Delhi  | 2020-01-01 | 2024-03-17 | FALSE  ← expired
2  | Animesh | Mumbai | 2024-03-18 | 9999-12-31 | TRUE   ← new current

USE WHEN: Full history needed (sales analysis by customer's city at order time)
```

```sql
-- Step 1: expire old record
UPDATE dim_customer
SET valid_to = CURRENT_DATE - 1, is_current = FALSE
WHERE customer_id = 'CUST_101' AND is_current = TRUE;

-- Step 2: insert new record
INSERT INTO dim_customer
  (customer_id, name, city, valid_from, valid_to, is_current)
VALUES ('CUST_101', 'Animesh', 'Mumbai', CURRENT_DATE, '9999-12-31', TRUE);
```

---

### SCD Type 3 — New Column

```
Before:  sk | name    | city
         1  | Animesh | Delhi

After:   sk | name    | city   | prev_city
         1  | Animesh | Mumbai | Delhi

USE WHEN: Only "before & after" matters, not full history
```

```sql
ALTER TABLE dim_customer ADD COLUMN prev_city VARCHAR(50);
UPDATE dim_customer SET prev_city = city, city = 'Mumbai' WHERE customer_sk = 1;
```

---

### SCD Type 4 — History Table

```
dim_customer (current only):         dim_customer_history (all changes):
sk | name    | city                  sk | name    | city   | changed_date
1  | Animesh | Mumbai                1  | Animesh | Delhi  | 2020-01-01
                                     1  | Animesh | Mumbai | 2024-03-18

USE WHEN: Keep current table fast + separate full history table
```

---

### SCD Type 6 — Hybrid (1+2+3)

```
sk | name    | city   | prev_city | valid_from | valid_to   | is_current
1  | Animesh | Delhi  | NULL      | 2020-01-01 | 2024-03-17 | FALSE
2  | Animesh | Mumbai | Delhi     | 2024-03-18 | 9999-12-31 | TRUE

Has:  current value (Type 1 behavior on current row)
      full history (Type 2 — new rows)
      previous value (Type 3 — prev_city column)

USE WHEN: Maximum flexibility needed (complex reporting requirements)
```

---

### SCD Quick Summary

| Type | History? | How | Common? |
|------|----------|-----|---------|
| Type 1 | ❌ No | Overwrite | Simple corrections |
| Type 2 | ✅ Full | New row per change | ✅ Most common in DWH |
| Type 3 | ⚠️ Partial | New column | Limited "before/after" |
| Type 4 | ✅ Full | Separate history table | When main table must stay clean |
| Type 6 | ✅ Full + partial | New row + column | Maximum flexibility |

> **Q: Which SCD type is most asked in interviews?**
> Type 2 — understand it deeply. Type 1 and 3 as supporting knowledge.

---

## 9. Data Vault — Just Enough

> A more recent modelling approach designed for **agility and auditability**.
> You don't need to implement it at 0-2yr level — but you should know what it is.

```
Data Vault has 3 building blocks:

HUB      → Stores unique business keys (the "what")
LINK     → Stores relationships between hubs (the "connection")
SATELLITE→ Stores descriptive attributes + history (the "detail")
```

```
hub_customer        link_customer_order       hub_order
┌──────────────┐    ┌─────────────────────┐  ┌──────────────┐
│customer_hk PK│───►│customer_hk FK       │  │order_hk  PK  │
│customer_bk   │    │order_hk    FK       │◄─┤order_bk      │
│load_date     │    │load_date            │  │load_date     │
│record_source │    │record_source        │  │record_source │
└──────┬───────┘    └─────────────────────┘  └──────────────┘
       │
sat_customer
┌──────────────┐
│customer_hk FK│
│load_date     │
│name          │
│city          │
│is_current    │
└──────────────┘
```

| | Kimball | Data Vault |
|--|---------|------------|
| Best for | BI / dashboards | Auditability, frequent source changes |
| Complexity | Medium | Higher |
| History tracking | SCD Type 2 | Built-in (satellites) |
| Load style | Batch | Parallel, insert-only |
| Common at | Most companies | Banks, regulated industries |

> **Interview answer for "What is Data Vault?"**
> "A modelling methodology that separates business keys (Hubs), relationships (Links),
> and attributes (Satellites). It's more flexible than Kimball for changing sources
> and provides full audit history by design."

---

## 10. OLTP vs OLAP — Modelling Perspective

```
OLTP Model:                        OLAP Model (DWH):
(3NF normalized)                   (Star schema denormalized)

orders                             fact_sales
├── order_id PK                    ├── sale_sk PK
├── customer_id FK ──► customers   ├── customer_sk FK ──► dim_customer
├── product_id FK  ──► products    ├── product_sk  FK ──► dim_product
├── status                         ├── date_sk     FK ──► dim_date
└── created_at                     ├── amount
                                   └── quantity
Many small tables                  Few large tables
Fast writes                        Fast reads
Row-based storage                  Column-based storage (Redshift, BigQuery)
```

**Why different models?**

```
OLTP query:  "Get order #12345 details" → point lookup, 1 row
OLAP query:  "Total revenue by region for Q1 2024" → scan millions of rows

Same normalized model is TERRIBLE for OLAP:
→ Needs 10+ JOINs for a simple revenue report
→ Full table scans on huge tables
→ Analysts get confused by complex schema

Star schema solves this:
→ 3-4 JOINs maximum
→ Columnar scan on fact table
→ Analyst-friendly: "JOIN dim_date and GROUP BY month"
```

---

## 11. Grain — The Most Important Concept

> **Grain = what one row in a fact table represents.**
> Getting grain wrong is the #1 mistake in data modelling.

```
WRONG (mixed grain):
fact_sales has rows for:
  - individual line items (1 row per product per order)
  - order totals (1 row per order)
  - daily summaries (1 row per day)
→ Impossible to query correctly. SUM gives wrong numbers.

RIGHT (consistent grain):
fact_sales: one row = one line item on one invoice
→ Every row at the same level of detail
→ SUM(amount) always makes sense
```

**Grain examples:**

| Fact Table | Grain (1 row = ?) |
|------------|------------------|
| `fact_sales` | One line item on one order |
| `fact_daily_sales` | One day's total sales per store |
| `fact_inventory` | Inventory snapshot per product per day |
| `fact_sessions` | One user session |
| `fact_page_views` | One page view event |

> **Q: Why is grain so important?**
> It determines what questions you can answer.
> Fine grain (line item) → can roll up to any level.
> Coarse grain (daily total) → can't drill down to individual transactions.
> Always go as fine-grained as storage and performance allow.

> **Q: What is a factless fact table?**
> A fact table with no numeric measures — just foreign keys recording that an event happened.

```sql
-- factless fact: records student attendance (no numbers needed)
CREATE TABLE fact_attendance (
  student_sk INT,
  course_sk  INT,
  date_sk    INT,
  -- no measures! just the fact that student attended
  PRIMARY KEY (student_sk, course_sk, date_sk)
);
```

---

## 12. Interview Q&A Fire Round ⚡

> **Q: What is data modelling?**
> Designing how data is structured, stored, and related — so it's queryable, trustworthy, and fast.

> **Q: What is the difference between a fact table and a dimension table?**
> Fact = measurable numeric events (amounts, counts, durations).
> Dimension = descriptive context (who, what, when, where).

> **Q: What is grain and why does it matter?**
> Grain = what one row represents. Wrong grain = wrong aggregations. Always define grain first.

> **Q: Star schema vs Snowflake schema?**
> Star = denormalized dimensions, fewer JOINs, faster queries.
> Snowflake = normalized dimensions, more JOINs, saves storage.
> Star is preferred for analytics.

> **Q: What is a conformed dimension?**
> A dimension shared across multiple fact tables with the same definition.
> e.g. `dim_date` used in fact_sales AND fact_returns — same date meaning everywhere.

> **Q: What is SCD Type 2 and when do you use it?**
> Add a new row for each change with `valid_from`, `valid_to`, `is_current`.
> Use when full history must be preserved (customer address at time of purchase).

> **Q: Why use surrogate keys in a DWH?**
> Natural keys from source can change, be null, or be non-numeric (slow JOINs).
> Surrogate = stable integer, never null, fast to join.

> **Q: What is a degenerate dimension?**
> A dimension key with no separate dimension table — stored directly in fact table.
> e.g. `order_id` in fact_sales. No useful attributes beyond the key itself.

> **Q: What is a junk dimension?**
> Low-cardinality flags and indicators grouped into one dimension table.
> e.g. `is_promotional`, `is_online`, `payment_type` → `dim_transaction_type`

> **Q: What is the difference between additive, semi-additive, and non-additive facts?**
> Additive: SUM across all dims (sales_amount).
> Semi-additive: SUM across some dims, AVG across others (account_balance — don't sum over time).
> Non-additive: cannot be summed (ratios, percentages).

> **Q: What is a factless fact table?**
> Fact table with only FK columns — records that an event occurred, no measures.
> e.g. student course attendance, product promotion coverage.

> **Q: What is Data Vault?**
> Modelling methodology with Hubs (business keys), Links (relationships), Satellites (attributes).
> Built for auditability and handling frequent source system changes.

> **Q: Kimball vs Inmon approach?**
> Kimball = bottom-up, build data marts first, star schema, business-user focused.
> Inmon = top-down, build enterprise DWH in 3NF first, then data marts.
> Kimball is more common in modern practice.

---

*🗄️ Data Modelling Concepts · Core theory · 0-2yr DE interview ready*
