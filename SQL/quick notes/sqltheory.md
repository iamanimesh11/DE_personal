# 📘 SQL Theory Cheatsheet — Quick Revision Edition

> **23 topics** · Pattern-first · Interview-ready · With diagrams & examples

---

## 📑 Table of Contents

| # | Topic |
|---|-------|
| 1 | [Joins](#1-joins) |
| 2 | [WHERE vs HAVING](#2-where-vs-having) |
| 3 | [Primary Key vs Foreign Key](#3-primary-key-vs-foreign-key) |
| 4 | [Normalization](#4-normalization) |
| 5 | [Indexes](#5-indexes) |
| 6 | [ACID Properties](#6-acid-properties-transactions) |
| 7 | [DELETE vs TRUNCATE vs DROP](#7-delete-vs-truncate-vs-drop) |
| 8 | [Subquery vs JOIN](#8-subquery-vs-join) |
| 9 | [UNION vs UNION ALL](#9-union-vs-union-all) |
| 10 | [NULL Handling](#10-null-handling) |
| 11 | [Stored Procedures vs Functions](#11-stored-procedures-vs-functions) |
| 12 | [VIEW vs Materialized View](#12-view-vs-materialized-view) |
| 13 | [Window Functions — Theory](#13-window-functions--theory) |
| 14 | [CTE & Recursive CTE](#14-cte-common-table-expression) |
| 15 | [SQL Execution Order](#15-sql-execution-order) |
| 16 | [Constraints](#16-constraints) |
| 17 | [Quick Interview Fire Round](#17-quick-interview-fire-round) |
| 18 | [Triggers](#18-triggers) |
| 19 | [Star vs Snowflake Schema](#19-schema-design--star-vs-snowflake) |
| 20 | [OLTP vs OLAP](#20-oltp-vs-olap) |
| 21 | [Locks & Isolation Levels](#21-locks--isolation-levels) |
| 22 | [EXPLAIN / Query Plan](#22-explain--query-plan) |
| 23 | [String & Date Functions](#23-string--date-functions) |

---

## 1. Joins

```
Table A          Table B
┌────────┐       ┌────────┐
│ 1  ✓  │◄─────►│ 1  ✓  │  ← INNER JOIN  (only matching)
│ 2  ✓  │◄─────►│ 2  ✓  │
│ 3     │       │        │  ← LEFT JOIN   (all of A, NULL for B)
│        │       │ 4     │  ← RIGHT JOIN  (all of B, NULL for A)
└────────┘       └────────┘
         ↕ both sides = FULL OUTER JOIN
```

| Type | What it returns |
|------|----------------|
| `INNER JOIN` | Only matching rows in **both** tables |
| `LEFT JOIN` | All rows from left + matching from right *(NULL if no match)* |
| `RIGHT JOIN` | All rows from right + matching from left *(NULL if no match)* |
| `FULL OUTER JOIN` | All rows from both, NULL where no match |
| `CROSS JOIN` | Every combination — cartesian product |
| `SELF JOIN` | Table joined with itself |

> **Q: Difference between LEFT JOIN and INNER JOIN?**
> `INNER` returns only matches. `LEFT` returns ALL left rows even if no match on right.

> **Q: Can JOIN produce duplicate rows?**
> Yes — if one row in left matches multiple rows in right.

> **Q: What is a self join? When to use?**
> Joining a table to itself. Used for hierarchies (employee → manager) or comparing rows in same table.

```sql
-- Self join example: find employee and their manager
SELECT e.name AS employee, m.name AS manager
FROM emp e
LEFT JOIN emp m ON e.manager_id = m.id;
```

---

## 2. WHERE vs HAVING

```
Raw Rows → [ WHERE filters rows ] → GROUP BY → [ HAVING filters groups ] → Result
```

| Clause | Filters | Works on | Runs |
|--------|---------|----------|------|
| `WHERE` | Individual rows | Raw columns | Before GROUP BY |
| `HAVING` | Groups | Aggregates (SUM, COUNT…) | After GROUP BY |

```sql
-- WHERE: filter before grouping
SELECT dept, COUNT(*) FROM emp
WHERE salary > 30000          -- ✅ raw column
GROUP BY dept
HAVING COUNT(*) > 2;          -- ✅ aggregate
```

> **Q: Can you use aggregate functions in WHERE?**
> ❌ NO. Use `HAVING` for aggregates.

> **Q: Can HAVING be used without GROUP BY?**
> ✅ Yes — treats entire result as one group.

---

## 3. Primary Key vs Foreign Key

```
customers                    orders
┌─────────────────┐          ┌──────────────────────┐
│ customer_id  PK │◄────────►│ order_id  PK          │
│ name            │    FK    │ customer_id  FK ──────┘
│ city            │          │ amount                │
└─────────────────┘          └──────────────────────┘
```

| Key | Rule |
|-----|------|
| **Primary Key** | Uniquely identifies each row. NOT NULL. One per table. |
| **Foreign Key** | References PK of another table. Ensures referential integrity. |
| **Unique Key** | Like PK but allows ONE NULL. Multiple per table allowed. |

> **Q: Can a table have multiple primary keys?**
> ❌ NO — only one PK, but it can be **composite** (multi-column).

> **Q: Can a foreign key have NULL?**
> ✅ YES — means "no relationship" for that row.

---

## 4. Normalization

```
1NF → 2NF → 3NF → BCNF
 ↑      ↑      ↑      ↑
No    No     No     Every
repeat partial transitive determinant
groups depend. depend. = candidate key
```

| Form | Rule |
|------|------|
| **1NF** | No repeating groups. Each cell = atomic (single) value |
| **2NF** | 1NF + No partial dependency *(non-key col must depend on FULL PK)* |
| **3NF** | 2NF + No transitive dependency *(non-key col must not depend on another non-key col)* |
| **BCNF** | Stricter 3NF — every determinant must be a candidate key |

**Transitive dependency example:**
```
order_id → customer_id → customer_city   ← violates 3NF!
           (customer_city depends on customer_id, not directly on order_id)
```

> **Q: What is denormalization? Why do it?**
> Intentionally adding redundancy for query performance (fewer JOINs). Common in data warehouses.

---

## 5. Indexes

```
Without Index:              With Index (B-Tree):
Scan all 1M rows            Jump directly to matching rows
[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] slow    [   →→→ target] fast
```

| Type | Use |
|------|-----|
| **Clustered** | Sorts the actual table data. One per table. |
| **Non-Clustered** | Separate pointer structure. Multiple allowed. |
| **Composite** | Index on multiple columns. |
| **Unique** | Enforces uniqueness on column(s). |
| **Full-Text** | For text search (LIKE is slow, this is fast). |

> **Q: When should you NOT use an index?**
> Small tables · Low cardinality columns (e.g. `gender`) · Heavily updated columns

> **Q: Does an index slow down anything?**
> ✅ YES — `INSERT / UPDATE / DELETE` become slower (index must also be updated).

> **Q: What is a covering index?**
> An index that includes ALL columns needed for a query — avoids hitting the main table entirely.

---

## 6. ACID Properties (Transactions)

```
Bank Transfer: A → B  (₹1000)
┌─────────────────────────────────────┐
│  BEGIN                              │
│  UPDATE A SET balance = balance-1000│
│  UPDATE B SET balance = balance+1000│
│  COMMIT  ← success: both happen     │
│  ─ OR ─                             │
│  ROLLBACK ← failure: neither happen │
└─────────────────────────────────────┘
```

| Property | Meaning |
|----------|---------|
| **Atomicity** | All or nothing — either all steps succeed or none do |
| **Consistency** | DB moves from one valid state to another |
| **Isolation** | Concurrent transactions don't interfere with each other |
| **Durability** | Committed data survives crashes (written to disk) |

> **Q: What is a SAVEPOINT?**
> A checkpoint within a transaction. Can rollback to it without undoing everything.

```sql
BEGIN;
  INSERT INTO orders ...;
  SAVEPOINT sp1;
  UPDATE inventory ...;
ROLLBACK TO sp1;   -- only undoes UPDATE, INSERT stays
COMMIT;
```

---

## 7. DELETE vs TRUNCATE vs DROP

| Command | Removes | WHERE? | Rollback? | Resets AUTO_INCREMENT? |
|---------|---------|--------|-----------|------------------------|
| `DELETE` | Specific rows | ✅ YES | ✅ YES | ❌ NO |
| `TRUNCATE` | All rows | ❌ NO | ❌ NO | ✅ YES |
| `DROP` | Entire table | ❌ NO | ❌ NO | ✅ YES *(table gone)* |

```
DELETE   → surgical 🔪  (row by row, logged)
TRUNCATE → bulldoze 🏗️  (wipes all, fast)
DROP     → demolish 💣  (table ceases to exist)
```

> **Q: Which is faster — DELETE or TRUNCATE?**
> `TRUNCATE` — it doesn't log individual row deletions.

---

## 8. Subquery vs JOIN

```
Subquery (nested):               JOIN (flat):
SELECT *                         SELECT e.*
FROM emp                         FROM emp e
WHERE dept_id IN (               JOIN dept d
  SELECT id FROM dept            ON e.dept_id = d.id
  WHERE name = 'HR'              WHERE d.name = 'HR';
);
```

| Type | Description |
|------|-------------|
| **Scalar** | Returns single value — used in `SELECT` |
| **Row** | Returns single row |
| **Table** | Returns multiple rows/cols — used in `FROM` as derived table |
| **Correlated** | References outer query — runs once **per row** ⚠️ slow! |

> **Q: When is correlated subquery used?**
> When inner query depends on outer query's current row.
> e.g. *Find employees earning more than their dept average.*

```sql
-- Correlated subquery example
SELECT name, salary FROM emp e
WHERE salary > (
  SELECT AVG(salary) FROM emp
  WHERE dept_id = e.dept_id   -- references outer 'e'
);
```

---

## 9. UNION vs UNION ALL

```
Query A results:  [1, 2, 3]
Query B results:  [2, 3, 4]

UNION     → [1, 2, 3, 4]      (deduped — slower)
UNION ALL → [1, 2, 3, 2, 3, 4] (all rows — faster)
```

| | UNION | UNION ALL |
|--|-------|-----------|
| Duplicates | Removed | Kept |
| Speed | Slower (does DISTINCT) | Faster |
| Use when | Data may overlap | No duplicates expected |

> **Rule:** Both queries must have **same number of columns** with compatible types.

---

## 10. NULL Handling

```
NULL ≠ 0
NULL ≠ ''  (empty string)
NULL = "unknown / missing"

NULL = NULL  →  NULL  ❌ (not TRUE!)
NULL IS NULL →  TRUE  ✅
```

| Function | Behaviour |
|----------|-----------|
| `COALESCE(a, b, c)` | Returns **first non-NULL** value |
| `IFNULL(a, b)` | Returns `b` if `a` is NULL *(MySQL)* |
| `NULLIF(a, b)` | Returns NULL if `a = b`, else returns `a` |

```sql
SELECT COALESCE(phone, email, 'no contact') AS contact FROM users;
-- Returns phone if exists, else email, else 'no contact'
```

> **Q: Does COUNT(*) include NULLs?**
> `COUNT(*)` ✅ counts all rows. `COUNT(column)` ❌ skips NULLs.

---

## 11. Stored Procedures vs Functions

| | Stored Procedure | Function |
|--|-----------------|----------|
| **Returns** | 0 or more values | Exactly ONE value |
| **Used in SELECT** | ❌ Cannot | ✅ Can |
| **Transactions** | ✅ Supports | ❌ No |
| **Side effects** | Can INSERT/UPDATE | Should not (pure logic) |
| **Call** | `CALL proc_name()` | `SELECT func_name()` |

```sql
-- Function: used inline in SELECT
SELECT calculate_tax(salary) FROM emp;

-- Procedure: called separately
CALL generate_monthly_report('2024-01');
```

> **Q: When to use a stored procedure?**
> For complex business logic, batch operations, or reusable multi-step SQL.

---

## 12. VIEW vs Materialized View

```
Regular View:                 Materialized View:
┌─────────────┐               ┌─────────────┐
│  SELECT...  │  ← runs       │  Snapshot   │  ← stored on disk
│  every time │    on call    │  refreshed  │    periodically
└─────────────┘               └─────────────┘
  Always fresh                  Faster reads
  Slower on big queries         Slightly stale
```

> **Q: Can you INSERT into a view?**
> Only if view is based on a **single table** and has no aggregates / DISTINCT / GROUP BY.

> **Q: When to use Materialized View?**
> For expensive, frequently-run queries where real-time freshness is not critical.

---

## 13. Window Functions — Theory

```
GROUP BY collapses rows:         Window Function keeps all rows:
dept   salary                    name    dept   salary   avg_salary
HR     ──────► AVG = 50k         Alice   HR     60k      50k
IT     ──────► AVG = 70k         Bob     HR     40k      50k  ← row preserved!
                                 Carol   IT     70k      70k
```

> **Q: What is a window function?**
> Performs calculation across related rows WITHOUT collapsing them (unlike GROUP BY).

**RANK vs DENSE_RANK vs ROW_NUMBER:**

```
Salary: 100, 100, 80, 70

ROW_NUMBER  →  1, 2, 3, 4   (always unique, no ties)
RANK        →  1, 1, 3, 4   (ties get same rank, gap after)
DENSE_RANK  →  1, 1, 2, 3   (ties get same rank, NO gap)
```

> **Q: What does PARTITION BY do?**
> Splits data into groups (like GROUP BY) but keeps all rows visible.

> **Q: Default frame for `SUM() OVER (ORDER BY col)`?**
> `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

---

## 14. CTE (Common Table Expression)

```sql
-- Without CTE (messy nested subquery):
SELECT * FROM (SELECT *, ROW_NUMBER() OVER (...) rn FROM emp) t WHERE rn = 1;

-- With CTE (clean & readable):
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) rn
  FROM emp
)
SELECT * FROM ranked WHERE rn = 1;
```

> **Q: CTE vs Subquery — when to prefer CTE?**
> CTE is more readable, reusable within same query, and supports **recursion**.

**Recursive CTE — Employee → Manager hierarchy:**

```sql
WITH RECURSIVE org AS (
  SELECT id, name, manager_id, 1 AS level
  FROM emp WHERE manager_id IS NULL          -- anchor: CEO

  UNION ALL

  SELECT e.id, e.name, e.manager_id, o.level + 1
  FROM emp e
  JOIN org o ON e.manager_id = o.id          -- recursive step
)
SELECT * FROM org;
```

```
CEO (level 1)
 ├── VP Sales (level 2)
 │    └── Sales Rep (level 3)
 └── VP Tech (level 2)
      └── Engineer (level 3)
```

---

## 15. SQL Execution Order

```
① FROM / JOIN    ← get the data
② WHERE          ← filter rows
③ GROUP BY       ← group them
④ HAVING         ← filter groups
⑤ SELECT         ← pick columns
⑥ DISTINCT       ← remove dupes
⑦ ORDER BY       ← sort
⑧ LIMIT / OFFSET ← paginate
```

> **Q: Why can't you use SELECT alias in WHERE?**
> Because `WHERE` runs **before** `SELECT` — the alias doesn't exist yet.

> **Q: Can you ORDER BY a column not in SELECT?**
> ✅ YES — `ORDER BY` runs after `FROM/WHERE`, has access to all columns.

---

## 16. Constraints

| Constraint | Purpose |
|------------|---------|
| `PRIMARY KEY` | Unique + NOT NULL identifier |
| `FOREIGN KEY` | Referential integrity between tables |
| `UNIQUE` | No duplicate values *(allows one NULL)* |
| `NOT NULL` | Column must always have a value |
| `CHECK` | Custom condition must be true |
| `DEFAULT` | Assigns value if none provided |

```sql
CREATE TABLE orders (
  order_id   INT PRIMARY KEY,
  customer_id INT NOT NULL,
  status     VARCHAR(20) DEFAULT 'Pending',
  amount     DECIMAL CHECK (amount > 0),
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

> **Q: Can CHECK constraint reference another table?**
> ❌ NO — for cross-table rules, use triggers or application logic.

---

## 17. Quick Interview Fire Round ⚡

| Question | Answer |
|----------|--------|
| What is a composite key? | PK made of 2+ columns together |
| What is referential integrity? | FK value must exist in referenced PK — no orphan records |
| What is a deadlock? | Two transactions blocking each other. DB kills one to resolve. |
| What is cardinality? | Unique values in a column. HIGH = good for indexes. |
| Surrogate vs Natural key? | Surrogate = artificial ID (no business meaning). Natural = real-world value. |
| What is the N+1 problem? | 1 query → N records → N more queries. Fix: use JOIN instead. |
| What does EXPLAIN do? | Shows query execution plan — indexes used, rows scanned. |

---

## 18. Triggers

```
INSERT/UPDATE/DELETE on table
         ↓
  ┌─────────────┐
  │   TRIGGER   │  fires automatically
  └─────────────┘
         ↓
  BEFORE → validate / transform data
  AFTER  → audit log / sync another table
```

| Timing | Event | Use case |
|--------|-------|----------|
| `BEFORE` | INSERT / UPDATE | Validate or modify data before save |
| `AFTER` | INSERT / UPDATE / DELETE | Audit log, sync another table |

```sql
-- Audit log trigger example
CREATE TRIGGER after_order_insert
AFTER INSERT ON orders
FOR EACH ROW
  INSERT INTO audit_log(action, order_id, ts)
  VALUES ('INSERT', NEW.order_id, NOW());
```

> **Q: Trigger vs Stored Procedure?**
> Trigger fires **automatically** on table event. Procedure is called **explicitly**.

---

## 19. Schema Design — Star vs Snowflake

**Star Schema** *(preferred for analytics)*
```
         dim_date
            │
dim_customer─┤
            Fact_Sales ──── dim_product
dim_region──┤
            │
         dim_store
```
- Fact table at center, dimensions directly connected
- Denormalized · Fewer JOINs · Faster queries

**Snowflake Schema**
```
dim_product ──► dim_category ──► dim_subcategory
```
- Dimension tables normalized into sub-dimensions
- More JOINs · Saves storage · Harder to query

| | Star | Snowflake |
|--|------|-----------|
| JOINs needed | Few | Many |
| Query speed | Faster | Slower |
| Storage | More | Less |
| Best for | BI / dashboards | Large DWH with strict storage limits |

> **Q: Fact vs Dimension table?**
> **Fact** = measurable events (sales, clicks, transactions).
> **Dimension** = descriptive context (customer, product, date, location).

---

## 20. OLTP vs OLAP

```
OLTP                              OLAP
(Online Transaction Processing)   (Online Analytical Processing)

User clicks "Buy" → INSERT        Analyst runs → SELECT AVG, SUM, COUNT
Fast, small writes                Slow, large reads
Normalized tables                 Denormalized / star schema
MySQL, PostgreSQL                 Redshift, BigQuery, Snowflake
```

| | OLTP | OLAP |
|--|------|------|
| Purpose | Day-to-day transactions | Analytics / reporting |
| Operations | INSERT / UPDATE / DELETE | Mostly SELECT |
| Data volume | Small per query | Large scans |
| Normalization | Highly normalized (3NF) | Denormalized |
| Example | Banking, e-commerce | Data warehouse, BI dashboard |

> **Q: Can you run analytics on OLTP directly?**
> Technically yes — but it kills transaction performance. That's why ETL → OLAP exists.

---

## 21. Locks & Isolation Levels

**The three read problems:**
```
Dirty Read          → Txn A reads uncommitted data from Txn B (which may rollback)
Non-Repeatable Read → Txn A reads same row twice, gets different values (Txn B updated)
Phantom Read        → Txn A runs same query twice, gets different ROWS (Txn B inserted)
```

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|-----------------|------------|---------------------|--------------|
| `READ UNCOMMITTED` | ✅ YES | ✅ YES | ✅ YES |
| `READ COMMITTED` | ❌ NO | ✅ YES | ✅ YES |
| `REPEATABLE READ` | ❌ NO | ❌ NO | ✅ YES |
| `SERIALIZABLE` | ❌ NO | ❌ NO | ❌ NO |

*⬆ More protection = more locking = slower concurrency*

> **Q: Default isolation level in MySQL?**
> `REPEATABLE READ`

> **Q: Pessimistic vs Optimistic lock?**
> **Pessimistic** = lock the row immediately → `SELECT ... FOR UPDATE`
> **Optimistic** = no lock, check version/timestamp at commit time

---

## 22. EXPLAIN / Query Plan

```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 5;
```

```
+----+-------+------+------+---------+------+----------+
| id | type  | key  | rows | filtered | ref  | Extra    |
+----+-------+------+------+----------+------+----------+
|  1 | ref   | idx  |   3  |  100.00  | const|          |  ← GOOD (index used)
|  1 | ALL   | NULL | 10000|   10.00  |      |          |  ← BAD (full scan)
+----+-------+------+------+----------+------+----------+
```

| Column | What to look for |
|--------|-----------------|
| `type` | `ALL` = full scan 🔴. `ref/eq_ref/const` = index used 🟢 |
| `rows` | Estimated rows scanned — lower is better |
| `key` | Which index is being used |
| `Extra` | `Using filesort` or `Using temporary` = 🔴 red flags |

> **Q: EXPLAIN vs EXPLAIN ANALYZE?**
> `EXPLAIN` = estimated plan. `EXPLAIN ANALYZE` = actually runs query + shows real timings.

> **Q: What is a full table scan? Why bad?**
> DB reads every row. Fine for small tables, very slow on millions of rows. Fix: add index.

---

## 23. String & Date Functions

### String Functions

| Function | Example | Result |
|----------|---------|--------|
| `CONCAT(a, b)` | `CONCAT('Hello', ' World')` | `Hello World` |
| `SUBSTRING(str, pos, len)` | `SUBSTRING('Hello', 1, 3)` | `Hel` |
| `LENGTH(str)` | `LENGTH('Hello')` | `5` |
| `UPPER / LOWER` | `UPPER('hello')` | `HELLO` |
| `TRIM(str)` | `TRIM('  hi  ')` | `hi` |
| `REPLACE(str, a, b)` | `REPLACE('abcabc','a','X')` | `XbcXbc` |
| `LIKE` | `name LIKE 'A%'` | starts with A |

```
LIKE patterns:
  %  → any number of chars    ('A%' = starts with A