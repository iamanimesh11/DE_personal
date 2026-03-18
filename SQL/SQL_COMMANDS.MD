# 🗂️ SQL Commands Cheatsheet — DDL · DML · DCL · TCL

> All 4 command types · Syntax + Examples · Interview-ready

---

## 📑 Quick Map

```
SQL Commands
├── DDL  (Data Definition Language)   → Structure  → CREATE, ALTER, DROP, TRUNCATE, RENAME
├── DML  (Data Manipulation Language) → Data       → SELECT, INSERT, UPDATE, DELETE, MERGE
├── DCL  (Data Control Language)      → Access     → GRANT, REVOKE
└── TCL  (Transaction Control Language) → Transactions → BEGIN, COMMIT, ROLLBACK, SAVEPOINT
```

---

## 1. 🏗️ DDL — Data Definition Language

> **Defines / modifies the structure of tables and objects.**
> Changes are **auto-committed** — cannot be rolled back!

---

### CREATE

```sql
-- Create a table
CREATE TABLE employees (
  emp_id     INT          PRIMARY KEY AUTO_INCREMENT,
  name       VARCHAR(100) NOT NULL,
  dept       VARCHAR(50),
  salary     DECIMAL(10,2),
  joined_at  DATE         DEFAULT CURRENT_DATE
);

-- Create a database
CREATE DATABASE company_db;

-- Create an index
CREATE INDEX idx_dept ON employees(dept);

-- Create a view
CREATE VIEW high_earners AS
SELECT name, salary FROM employees WHERE salary > 80000;
```

---

### ALTER

```sql
-- Add a new column
ALTER TABLE employees ADD COLUMN email VARCHAR(100);

-- Drop a column
ALTER TABLE employees DROP COLUMN email;

-- Rename a column
ALTER TABLE employees RENAME COLUMN dept TO department;

-- Modify column type/size
ALTER TABLE employees MODIFY COLUMN name VARCHAR(200);

-- Add a constraint
ALTER TABLE employees ADD CONSTRAINT chk_salary CHECK (salary > 0);

-- Add foreign key
ALTER TABLE orders ADD FOREIGN KEY (emp_id) REFERENCES employees(emp_id);
```

---

### DROP

```sql
-- Drop a table (permanently gone ⚠️)
DROP TABLE employees;

-- Drop only if exists (safe)
DROP TABLE IF EXISTS employees;

-- Drop a database
DROP DATABASE company_db;

-- Drop an index
DROP INDEX idx_dept ON employees;

-- Drop a view
DROP VIEW high_earners;
```

---

### TRUNCATE

```sql
-- Remove ALL rows, keep table structure
TRUNCATE TABLE employees;
-- Faster than DELETE, resets AUTO_INCREMENT, cannot be rolled back
```

---

### RENAME

```sql
-- Rename a table
RENAME TABLE employees TO staff;

-- Alternative syntax (some DBs)
ALTER TABLE employees RENAME TO staff;
```

---

### DDL Quick Reference

| Command | Does | Rollback? | Auto-Commit? |
|---------|------|-----------|--------------|
| `CREATE` | Creates table/db/index/view | ❌ NO | ✅ YES |
| `ALTER` | Modifies table structure | ❌ NO | ✅ YES |
| `DROP` | Deletes object permanently | ❌ NO | ✅ YES |
| `TRUNCATE` | Removes all rows | ❌ NO | ✅ YES |
| `RENAME` | Renames a table | ❌ NO | ✅ YES |

---

## 2. ✏️ DML — Data Manipulation Language

> **Works with the data inside tables.**
> Changes can be rolled back (within a transaction).

---

### INSERT

```sql
-- Insert single row
INSERT INTO employees (name, dept, salary)
VALUES ('Animesh', 'Engineering', 95000);

-- Insert multiple rows
INSERT INTO employees (name, dept, salary) VALUES
  ('Priya',  'HR',          60000),
  ('Rahul',  'Finance',     72000),
  ('Sneha',  'Engineering', 88000);

-- Insert from another table
INSERT INTO archive_employees
SELECT * FROM employees WHERE joined_at < '2020-01-01';
```

---

### SELECT

```sql
-- Basic
SELECT name, salary FROM employees;

-- With condition
SELECT * FROM employees WHERE dept = 'Engineering';

-- With sorting
SELECT * FROM employees ORDER BY salary DESC;

-- With limit
SELECT * FROM employees ORDER BY salary DESC LIMIT 5;

-- With alias
SELECT name, salary * 12 AS annual_salary FROM employees;

-- With GROUP BY
SELECT dept, COUNT(*) AS headcount, AVG(salary) AS avg_sal
FROM employees
GROUP BY dept
HAVING COUNT(*) > 2;

-- With JOIN
SELECT e.name, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id;
```

---

### UPDATE

```sql
-- Update specific rows
UPDATE employees
SET salary = salary * 1.10
WHERE dept = 'Engineering';

-- Update multiple columns
UPDATE employees
SET salary = 90000,
    dept   = 'Data'
WHERE emp_id = 5;

-- Update using another table (JOIN)
UPDATE employees e
JOIN departments d ON e.dept_id = d.dept_id
SET e.salary = e.salary * 1.05
WHERE d.dept_name = 'HR';
```

> ⚠️ Always use `WHERE` in UPDATE — without it, ALL rows get updated!

---

### DELETE

```sql
-- Delete specific rows
DELETE FROM employees WHERE emp_id = 5;

-- Delete based on condition
DELETE FROM employees WHERE joined_at < '2018-01-01';

-- Delete using subquery
DELETE FROM orders
WHERE customer_id NOT IN (SELECT id FROM customers);
```

> ⚠️ Always use `WHERE` in DELETE — without it, ALL rows get deleted!

---

### MERGE (UPSERT)

```sql
-- Insert if not exists, Update if exists
MERGE INTO employees AS target
USING new_data AS source
ON target.emp_id = source.emp_id
WHEN MATCHED THEN
  UPDATE SET target.salary = source.salary
WHEN NOT MATCHED THEN
  INSERT (emp_id, name, salary)
  VALUES (source.emp_id, source.name, source.salary);
```

> MySQL alternative: `INSERT ... ON DUPLICATE KEY UPDATE`

```sql
INSERT INTO employees (emp_id, name, salary)
VALUES (5, 'Animesh', 95000)
ON DUPLICATE KEY UPDATE salary = 95000;
```

---

### DML Quick Reference

| Command | Does | Rollback? |
|---------|------|-----------|
| `SELECT` | Read data | N/A |
| `INSERT` | Add new rows | ✅ YES |
| `UPDATE` | Modify existing rows | ✅ YES |
| `DELETE` | Remove specific rows | ✅ YES |
| `MERGE` | Insert or update (upsert) | ✅ YES |

---

## 3. 🔐 DCL — Data Control Language

> **Controls who can access what in the database.**

---

### GRANT

```sql
-- Grant SELECT on a table to a user
GRANT SELECT ON employees TO 'animesh'@'localhost';

-- Grant multiple privileges
GRANT SELECT, INSERT, UPDATE ON employees TO 'animesh'@'localhost';

-- Grant all privileges on a database
GRANT ALL PRIVILEGES ON company_db.* TO 'animesh'@'localhost';

-- Grant with ability to pass it on
GRANT SELECT ON employees TO 'animesh'@'localhost' WITH GRANT OPTION;

-- Apply changes
FLUSH PRIVILEGES;
```

---

### REVOKE

```sql
-- Revoke specific privilege
REVOKE INSERT ON employees FROM 'animesh'@'localhost';

-- Revoke all privileges
REVOKE ALL PRIVILEGES ON company_db.* FROM 'animesh'@'localhost';
```

---

### DCL Quick Reference

```
Privileges you can GRANT / REVOKE:
┌────────────┬────────────────────────────────┐
│ SELECT     │ Read data                      │
│ INSERT     │ Add rows                       │
│ UPDATE     │ Modify rows                    │
│ DELETE     │ Remove rows                    │
│ CREATE     │ Create tables/databases        │
│ DROP       │ Delete tables/databases        │
│ INDEX      │ Create/drop indexes            │
│ ALL        │ All of the above               │
└────────────┴────────────────────────────────┘
```

| Command | Does |
|---------|------|
| `GRANT` | Give permission to user |
| `REVOKE` | Take permission away from user |

---

## 4. 🔄 TCL — Transaction Control Language

> **Controls how transactions are saved or undone.**
> Works with DML commands (INSERT / UPDATE / DELETE).

---

### Transaction Flow

```
BEGIN / START TRANSACTION
        │
        ├── INSERT / UPDATE / DELETE  ← your DML operations
        │
        ├── SAVEPOINT sp1             ← optional checkpoint
        │
        ├── more DML...
        │
        ├── COMMIT   ✅               ← save everything permanently
        │    OR
        └── ROLLBACK ❌               ← undo everything back to BEGIN
             OR
             ROLLBACK TO sp1          ← undo only back to savepoint
```

---

### BEGIN / START TRANSACTION

```sql
BEGIN;
-- or
START TRANSACTION;

  UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
  UPDATE accounts SET balance = balance + 1000 WHERE id = 2;

COMMIT;  -- both updates saved together
```

---

### COMMIT

```sql
BEGIN;
  INSERT INTO orders (customer_id, amount) VALUES (5, 1500);
  UPDATE inventory SET stock = stock - 1 WHERE product_id = 10;
COMMIT;  -- permanently writes both changes to disk
```

---

### ROLLBACK

```sql
BEGIN;
  DELETE FROM employees WHERE dept = 'HR';  -- oops, wrong query!
ROLLBACK;  -- undo! all deleted rows are restored
```

---

### SAVEPOINT

```sql
BEGIN;
  INSERT INTO orders VALUES (101, 5, 1500);   -- step 1
  SAVEPOINT after_insert;                      -- checkpoint

  UPDATE inventory SET stock = stock - 1;      -- step 2
  -- something went wrong in step 2...
  ROLLBACK TO after_insert;                    -- undo step 2 only, keep step 1

COMMIT;  -- saves only step 1
```

---

### RELEASE SAVEPOINT

```sql
-- Remove a savepoint (no longer needed)
RELEASE SAVEPOINT after_insert;
```

---

### SET AUTOCOMMIT

```sql
-- Check current setting
SELECT @@autocommit;

-- Disable autocommit (manual control)
SET autocommit = 0;

-- Enable autocommit (every statement commits immediately)
SET autocommit = 1;
```

> By default MySQL has `autocommit = 1` — every statement is its own transaction.
> Set to `0` when you want to group multiple statements into one transaction.

---

### TCL Quick Reference

| Command | Does |
|---------|------|
| `BEGIN` / `START TRANSACTION` | Starts a new transaction |
| `COMMIT` | Saves all changes permanently |
| `ROLLBACK` | Undoes all changes back to BEGIN |
| `SAVEPOINT name` | Creates a named checkpoint |
| `ROLLBACK TO name` | Undoes changes back to savepoint |
| `RELEASE SAVEPOINT name` | Removes a savepoint |
| `SET autocommit = 0/1` | Toggle auto-commit on/off |

---

### Real-world TCL Example — Bank Transfer

```sql
START TRANSACTION;

  -- Debit sender
  UPDATE accounts SET balance = balance - 5000
  WHERE account_id = 101;

  -- Check if sender has enough balance
  -- (application logic here — if insufficient, rollback)

  -- Credit receiver
  UPDATE accounts SET balance = balance + 5000
  WHERE account_id = 202;

  -- All good — commit
COMMIT;

-- If anything fails:
-- ROLLBACK;  ← neither debit nor credit happens
```

---

## 5. 🗺️ Full SQL Command Map

```
┌─────────────────────────────────────────────────────────────┐
│                      SQL COMMANDS                           │
├───────────┬──────────────┬────────────┬─────────────────────┤
│   DDL     │     DML      │    DCL     │        TCL          │
│ Structure │    Data      │   Access   │    Transactions     │
├───────────┼──────────────┼────────────┼─────────────────────┤
│ CREATE    │ SELECT       │ GRANT      │ BEGIN               │
│ ALTER     │ INSERT       │ REVOKE     │ COMMIT              │
│ DROP      │ UPDATE       │            │ ROLLBACK            │
│ TRUNCATE  │ DELETE       │            │ SAVEPOINT           │
│ RENAME    │ MERGE        │            │ RELEASE SAVEPOINT   │
├───────────┼──────────────┼────────────┼─────────────────────┤
│ Auto-     │ Rollback-    │ Permission │ Manual transaction  │
│ committed │ able         │ control    │ control             │
└───────────┴──────────────┴────────────┴─────────────────────┘
```

---

## 6. ⚡ Interview Q&A — Commands

> **Q: What is the difference between DDL and DML?**
> DDL changes **structure** (tables, columns). DML changes **data** (rows). DDL is auto-committed, DML can be rolled back.

> **Q: Can TRUNCATE be rolled back?**
> ❌ NO in MySQL. It's DDL — auto-committed. DELETE can be rolled back (it's DML).

> **Q: What happens if you COMMIT without a BEGIN?**
> In autocommit mode, each statement is already its own transaction — COMMIT has no extra effect.

> **Q: Difference between ROLLBACK and ROLLBACK TO SAVEPOINT?**
> `ROLLBACK` undoes **everything** back to BEGIN. `ROLLBACK TO sp` undoes only back to that savepoint.

> **Q: What is GRANT OPTION?**
> Allows the user to pass their granted privilege on to other users.

> **Q: What is autocommit?**
> When ON, every single SQL statement is automatically committed. Set to OFF for multi-statement transactions.

> **Q: Can SELECT be rolled back?**
> SELECT reads data — it doesn't modify anything, so there's nothing to roll back.

---

*🎯 DDL · DML · DCL · TCL — All 4 covered · Syntax-first · Interview-ready*
