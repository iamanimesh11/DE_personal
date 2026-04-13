# SQL Daily Drill — Day 1

---

## 🏢 Scenario: E-Commerce Order Platform — ShopX

---

## 📦 Tables & Sample Data

**customers**
| customer_id | name    | city      | signup_date |
|-------------|---------|-----------|-------------|
| 1           | Animesh | Delhi     | 2022-03-15  |
| 2           | Rohit   | Mumbai    | 2022-03-20  |
| 3           | Sneha   | Delhi     | 2023-07-01  |
| 4           | Karan   | Bangalore | 2021-11-10  |

**products**
| product_id | product_name | category    | price   | referred_by |
|------------|--------------|-------------|---------|-------------|
| 1          | Phone X      | Electronics | 15000   | NULL        |
| 2          | Phone Case   | Accessories | 300     | 1           |
| 3          | Laptop Pro   | Electronics | 75000   | NULL        |
| 4          | USB Hub      | Accessories | 800     | 3           |
| 5          | Screen Guard | Accessories | 150     | 2           |

**orders**
| order_id | customer_id | order_date | status    |
|----------|-------------|------------|-----------|
| 101      | 1           | 2024-01-10 | delivered |
| 102      | 1           | 2024-02-15 | returned  |
| 103      | 2           | 2024-01-20 | delivered |
| 104      | 3           | 2024-03-05 | pending   |
| 105      | 1           | 2024-04-01 | delivered |

**order_items**
| item_id | order_id | product_id | quantity | discount |
|---------|----------|------------|----------|----------|
| 1       | 101      | 1          | 1        | 10       |
| 2       | 101      | 2          | 2        | 0        |
| 3       | 102      | 3          | 1        | 5        |
| 4       | 103      | 1          | 1        | 0        |
| 5       | 104      | 4          | 3        | 15       |
| 6       | 105      | 5          | 5        | 0        |

> Revenue per item = `price × quantity × (1 - discount/100)`

---

## 📋 Problems

---

**Q1 — GROUP BY + HAVING**

Find total revenue per category. Show only categories where total revenue > ₹10,000. Sort descending.

| category    | total_revenue |
|-------------|---------------|
| Electronics | 84750.00      |

---

**Q2 — RANK within partition**

For each category, rank products by total quantity sold. Same quantity = same rank. Show top 2 per category.

| category    | product_name | total_qty | rnk |
|-------------|--------------|-----------|-----|
| Accessories | Screen Guard | 5         | 1   |
| Accessories | USB Hub      | 3         | 2   |
| Electronics | Phone X      | 2         | 1   |

---

**Q3 — LAG**

For each customer, list orders chronologically with days since their previous order. First order = NULL.

| customer_id | order_id | order_date | days_since_last |
|-------------|----------|------------|-----------------|
| 1           | 101      | 2024-01-10 | NULL            |
| 1           | 102      | 2024-02-15 | 36              |
| 1           | 105      | 2024-04-01 | 45              |
| 2           | 103      | 2024-01-20 | NULL            |

---

**Q4 — Cumulative Running Total**

For each customer, show cumulative revenue spent up to and including each order.

| customer_id | order_id | order_date | order_total | running_total |
|-------------|----------|------------|-------------|---------------|
| 1           | 101      | 2024-01-10 | 14100.00    | 14100.00      |
| 1           | 102      | 2024-02-15 | 71250.00    | 85350.00      |
| 1           | 105      | 2024-04-01 | 750.00      | 86100.00      |

---

**Q5 — CTE + Multi-condition Filter**

Find customers with more than 2 orders AND average order value > ₹5,000.

| customer_id | total_orders | avg_order_value |
|-------------|--------------|-----------------|
| 1           | 3            | 28700.00        |

---

**Q6 — Recursive CTE**

For product_id = 5 (Screen Guard), fetch its full ancestor chain using `referred_by` up to root.

| product_id | product_name | level |
|------------|--------------|-------|
| 5          | Screen Guard | 1     |
| 2          | Phone Case   | 2     |
| 1          | Phone X      | 3     |

---

**Q7 — Correlated Subquery**

Find customers whose most recent order has status = `'returned'`.

| customer_id | name    |
|-------------|---------|
| 1           | Animesh |

---

**Q8 — Subquery in FROM (Derived Table)**

Find the month (YYYY-MM) with the highest number of orders placed.

| month   | order_count |
|---------|-------------|
| 2024-01 | 2           |

---

**Q9 — CASE WHEN Pivot**

For each city, show delivered / returned / pending order counts as separate columns.

| city      | delivered | returned | pending |
|-----------|-----------|----------|---------|
| Delhi     | 2         | 1        | 1       |
| Mumbai    | 1         | 0        | 0       |

---

**Q10 — NTILE Bucketing**

Classify customers into 4 tiers by lifetime spend: Bronze (lowest) → Platinum (highest).

| customer_id | total_spend | tier     |
|-------------|-------------|----------|
| 3           | 2040.00     | Bronze   |
| 2           | 15000.00    | Silver   |
| 1           | 86100.00    | Platinum |

---

**Q11 — Self JOIN**

Find pairs of customers from the same city. Each pair appears only once (no A,B and B,A).

| customer_1 | customer_2 | city  |
|------------|------------|-------|
| 1          | 3          | Delhi |

---

**Q12 — RANK vs DENSE_RANK**

Rank all products by total revenue. Show RANK and DENSE_RANK side by side to see how ties differ.

| product_name | revenue  | rank | dense_rank |
|--------------|----------|------|------------|
| Laptop Pro   | 71250.00 | 1    | 1          |
| Phone X      | 13500.00 | 2    | 2          |
| Phone Case   | 600.00   | 3    | 3          |

---

**Q13 — FIRST_VALUE**

For each customer, show every order alongside the revenue of their very first order ever.

| customer_id | order_id | order_total | first_order_revenue |
|-------------|----------|-------------|---------------------|
| 1           | 101      | 14100.00    | 14100.00            |
| 1           | 102      | 71250.00    | 14100.00            |
| 1           | 105      | 750.00      | 14100.00            |

---

**Q14 — EXISTS vs IN**

Find customers with at least one returned order. Write using both `IN` and `EXISTS`.

| customer_id | name    |
|-------------|---------|
| 1           | Animesh |

---

**Q15 — PERCENT_RANK**

For each product, compute its percentile rank by revenue within its own category.

| product_name | category    | revenue  | pct_rank |
|--------------|-------------|----------|----------|
| Laptop Pro   | Electronics | 71250.00 | 1.0      |
| Phone X      | Electronics | 13500.00 | 0.0      |
| Screen Guard | Accessories | 750.00   | 1.0      |

---

**Q16 — NOT EXISTS / LEFT JOIN IS NULL**

Find products that have never been ordered. (Add a product with no orders in your local data to test.)

| product_id | product_name |
|------------|--------------|
| 6          | Webcam HD    |

---

**Q17 — Top N per customer**

For each customer, find their most expensive order by total value. Show tied orders too.

| customer_id | order_id | order_total |
|-------------|----------|-------------|
| 1           | 102      | 71250.00    |
| 2           | 103      | 15000.00    |

---

**Q18 — Month Completeness**

Find customers who placed at least one order in every month of 2024 (all 12 months covered).

| customer_id | name |
|-------------|------|
| *(extend sample data to 12 months to test this)* |

---

**Q19 — LEAD within partition**

For each item in an order, show the next product ordered within the same order_id. NULL if last.

| order_id | product_name | next_product |
|----------|--------------|--------------|
| 101      | Phone X      | Phone Case   |
| 101      | Phone Case   | NULL         |

---

**Q20 — 7-Day Rolling Average**

Compute 7-day rolling average of daily total revenue across the whole platform.

| order_date | daily_revenue | rolling_7day_avg |
|------------|---------------|------------------|
| 2024-01-10 | 14100.00      | 14100.00         |
| 2024-01-20 | 15000.00      | 14550.00         |
| 2024-02-15 | 71250.00      | ...              |

---
