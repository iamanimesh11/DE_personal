# 🧠 SQL INTERVIEW MIND-HACK CHEATSHEET (BIG MNC LEVEL)

> **Golden Rule:**  
> Interviews test **PATTERNS**, not syntax.

---

## 🔑 CORE PATTERN MAP (MOST IMPORTANT)

| Pattern | Typical Question | Example SQL |
|------|------------------|------------|
| **Previous / Next** | Compare current vs previous order | ```sql SELECT user_id, order_date, LAG(order_date) OVER (PARTITION BY user_id ORDER BY order_date) AS prev_order FROM orders; ``` |
| **Consecutive days** | Find login streaks | ```sql SELECT user_id, login_date FROM ( SELECT user_id, login_date, login_date - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp FROM logins ) t GROUP BY user_id, grp; ``` |
| **Time gap / delay** | Days between orders | ```sql SELECT user_id, DATEDIFF(order_date, LAG(order_date) OVER (PARTITION BY user_id ORDER BY order_date)) AS gap_days FROM orders; ``` |
| **Session / inactivity** | New session after 30 mins | ```sql SELECT *, CASE WHEN TIMESTAMPDIFF(MINUTE, LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time), event_time) > 30 THEN 1 ELSE 0 END AS new_session FROM events; ``` |
| **Top N per group** | Top 2 salaries per dept | ```sql SELECT * FROM ( SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) rn FROM emp ) t WHERE rn <= 2; ``` |
| **Retention / churn** | Month-1 retention | ```sql SELECT user_id FROM activity WHERE TIMESTAMPDIFF(MONTH, signup_date, activity_date) = 1; ``` |
| **Funnel / drop-off** | Signup → Purchase | ```sql SELECT user_id, MAX(CASE WHEN event='signup' THEN 1 END) signup, MAX(CASE WHEN event='purchase' THEN 1 END) purchase FROM events GROUP BY user_id; ``` |
| **Spike / anomaly** | Sudden jump in sales | ```sql SELECT day, (sales - LAG(sales) OVER (ORDER BY day)) / LAG(sales) OVER (ORDER BY day) AS pct_change FROM daily_sales; ``` |
| **Repeat users** | Users with multiple orders | ```sql SELECT user_id FROM orders GROUP BY user_id HAVING COUNT(*) > 1; ``` |
| **Running total** | Cumulative revenue | ```sql SELECT day, SUM(revenue) OVER (ORDER BY day) AS running_total FROM sales; ``` |

---

## ⏱️ TIME-BASED PROBLEMS (≈50% OF INTERVIEWS)

| Question | Example SQL |
|--------|-------------|
| Days between orders | ```sql SELECT user_id, DATEDIFF(order_date, LAG(order_date) OVER (PARTITION BY user_id ORDER BY order_date)) FROM orders; ``` |
| Inactive for 30 days | ```sql SELECT user_id FROM events GROUP BY user_id HAVING DATEDIFF(CURDATE(), MAX(event_date)) > 30; ``` |
| Rolling 7 days | ```sql SELECT day, SUM(sales) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) FROM sales; ``` |
| Month-1 retention | ```sql SELECT COUNT(DISTINCT user_id) FROM activity WHERE TIMESTAMPDIFF(MONTH, signup_date, activity_date) = 1; ``` |
| Session after 30 mins | ```sql CASE WHEN TIMESTAMPDIFF(MINUTE, prev_time, event_time) > 30 THEN 1 END ``` |

---

## 🧩 WINDOW FUNCTION QUICK DECISION TABLE

| Need | Example |
|----|--------|
| Previous row | ```sql LAG(amount) OVER (PARTITION BY user_id ORDER BY date) ``` |
| Next row | ```sql LEAD(amount) OVER (PARTITION BY user_id ORDER BY date) ``` |
| Unique rank | ```sql ROW_NUMBER() OVER (ORDER BY score DESC) ``` |
| Rank with ties | ```sql RANK() OVER (ORDER BY score DESC) ``` |
| Rank without gaps | ```sql DENSE_RANK() OVER (ORDER BY score DESC) ``` |
| Running total | ```sql SUM(amount) OVER (ORDER BY date) ``` |

---

## 📊 COHORT ANALYSIS MINI-MAP (WITH EXAMPLE)

**Question:** Month-wise retention by signup month

```sql
SELECT
  DATE_FORMAT(signup_date,'%Y-%m') AS cohort_month,
  TIMESTAMPDIFF(MONTH, signup_date, activity_date) AS months_since_signup,
  COUNT(DISTINCT user_id) AS active_users
FROM activity
GROUP BY 1,2;


# EXAMPLE

## 📊 Tables

---

## 🧑‍💼 `customers` TABLE (Sample Data)

| customer_id | customer_name | city        | signup_date |
|------------:|---------------|-------------|-------------|
| 1 | Amit Sharma   | Delhi     | 2022-01-10 |
| 2 | Anjali Verma  | Mumbai    | 2022-03-15 |
| 3 | Rahul Mehta   | Bangalore | 2021-11-20 |
| 4 | Sneha Iyer    | Chennai   | 2023-02-05 |
| 5 | Akash Singh  | Delhi     | 2023-06-18 |
| 6 | Priya Nair   | Kochi     | 2022-09-25 |
| 7 | Rohan Das    | Kolkata   | 2021-08-12 |
| 8 | Aditi Rao    | Mumbai    | 2023-01-02 |

---

## 📦 `orders` TABLE (Sample Data)

| order_id | customer_id | order_date | order_amount | status |
|---------:|------------:|------------|-------------:|--------|
| 101 | 1 | 2022-02-01 | 1200 | Completed |
| 102 | 1 | 2022-05-10 | 800  | Completed |
| 103 | 2 | 2022-06-15 | 450  | Cancelled |
| 104 | 2 | 2023-01-20 | 700  | Completed |
| 105 | 3 | 2021-12-01 | 3000 | Completed |
| 106 | 3 | 2022-07-22 | 1500 | Completed |
| 107 | 4 | 2023-02-10 | 2000 | Completed |
| 108 | 5 | 2023-07-01 | 600  | Pending   |
| 109 | 6 | 2022-10-05 | 900  | Completed |
| 110 | 6 | 2023-03-12 | 1100 | Completed |
| 111 | 8 | 2023-01-10 | 5000 | Completed |

---

## 💳 `payments` TABLE (Sample Data)

| payment_id | order_id | payment_date | payment_method | amount |
|-----------:|---------:|--------------|----------------|-------:|
| 1001 | 101 | 2022-02-02 | Credit Card | 1200 |
| 1002 | 102 | 2022-05-11 | UPI         | 800  |
| 1003 | 104 | 2023-01-21 | Debit Card  | 700  |
| 1004 | 105 | 2021-12-02 | Net Banking | 3000 |
| 1005 | 106 | 2022-07-23 | Credit Card | 1500 |
| 1006 | 107 | 2023-02-11 | UPI         | 2000 |
| 1007 | 109 | 2022-10-06 | Debit Card  | 900  |
| 1008 | 110 | 2023-03-13 | Credit Card | 1100 |
| 1009 | 111 | 2023-01-11 | Net Banking | 5000 |

---


## 🔹 QUESTION

Write SQL queries to:

1. Get customers who signed up after `2022-01-01`
2. Get completed orders with amount > 500
3. Get distinct customer cities
4. Total order amount per customer
5. Average order value per city
6. Number of orders per customer
7. Show customer name with their orders
8. Show all orders even if payment is missing
9. Find customers who never placed an order
10. Customers whose total order amount > 5000
11. Cities with more than 10 orders
12. Orders greater than average order amount
13. Customers whose first order was in 2023
14. Extract year & month from order_date
15. Customers whose name starts with 'A'
16. Days between signup and first order
17. Rank orders by amount per customer
18. Latest order per customer
19. Running total of order amount per customer
20. Second highest order per customer
21. Compare current order with previous order
22. Orders above city average
23. Percent contribution of each order to customer total
24. Top 3 customers by revenue
25. Categorize customers (Silver / Gold / Platinum)
26. Suggest indexes

---

# ✅ COMPLETE SQL SOLUTION

---

### 1️⃣ Customers after 2022-01-01
```sql
SELECT *
FROM customers
WHERE signup_date > '2022-01-01';
```

---

2️⃣ Completed orders > 500
```sql
SELECT *
FROM orders
WHERE status = 'Completed'
AND order_amount > 500;
```

---

3️⃣ Distinct cities
```sql
SELECT DISTINCT city
FROM customers;
```

---

4️⃣ Total order amount per customer
```sql
SELECT customer_id, SUM(order_amount) AS total_amount
FROM orders
GROUP BY customer_id;
```

---

5️⃣ Average order value per city
```sql
SELECT c.city, AVG(o.order_amount) AS avg_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city;
```

---

6️⃣ Orders count per customer
```sql
SELECT customer_id, COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id;
```

---

7️⃣ Customer name with orders
```sql
SELECT c.customer_name, o.order_id, o.order_date, o.order_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;
```

---

8️⃣ Orders even if payment missing
```sql
SELECT o.*, p.payment_id
FROM orders o
LEFT JOIN payments p ON o.order_id = p.order_id;
```

---

9️⃣ Customers with no orders
```sql
SELECT c.*
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

---

🔟 Customers with total > 5000
```sql
SELECT customer_id, SUM(order_amount) AS total_amount
FROM orders
GROUP BY customer_id
HAVING SUM(order_amount) > 5000;
```

---

1️⃣1️⃣ Cities with more than 10 orders
```sql
SELECT c.city, COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
HAVING COUNT(o.order_id) > 10;
```

---

1️⃣2️⃣ Orders above average
```sql
SELECT *
FROM orders
WHERE order_amount > (SELECT AVG(order_amount) FROM orders);
```

---

1️⃣3️⃣ First order in 2023
```sql
SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING MIN(order_date) BETWEEN '2023-01-01' AND '2023-12-31';
```

---

1️⃣4️⃣ Year & month extraction
```sql
SELECT
  EXTRACT(YEAR FROM order_date) AS year,
  EXTRACT(MONTH FROM order_date) AS month
FROM orders;
```

---

1️⃣5️⃣ Names starting with 'A'
```sql
SELECT *
FROM customers
WHERE customer_name LIKE 'A%';
```

---

1️⃣6️⃣ Days between signup & first order
```sql
SELECT c.customer_id,
       MIN(o.order_date) - c.signup_date AS days_gap
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.signup_date;
```

---

🪟 WINDOW FUNCTIONS


---

1️⃣7️⃣ Rank orders per customer
```sql
SELECT *,
RANK() OVER (PARTITION BY customer_id ORDER BY order_amount DESC) AS rank_no
FROM orders;
```

---

1️⃣8️⃣ Latest order per customer
```sql
SELECT *
FROM (
  SELECT *,
  ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
  FROM orders
) t
WHERE rn = 1;

```
---

1️⃣9️⃣ Running total
```sql
SELECT *,
SUM(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total
FROM orders;
```

---

2️⃣0️⃣ Second highest order
```sql
SELECT *
FROM (
  SELECT *,
  DENSE_RANK() OVER (PARTITION BY customer_id ORDER BY order_amount DESC) AS rnk
  FROM orders
) t
WHERE rnk = 2;

```
---

2️⃣1️⃣ Compare with previous order
```sql
SELECT *,
LAG(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order_amount
FROM orders;
```

---

2️⃣2️⃣ Orders above city average
```sql
SELECT *
FROM (
  SELECT o.*, c.city,
  AVG(order_amount) OVER (PARTITION BY city) AS city_avg
  FROM orders o
  JOIN customers c ON o.customer_id = c.customer_id
) t
WHERE order_amount > city_avg;
```

---

2️⃣3️⃣ Percent contribution
```sql
SELECT *,
(order_amount * 100.0) /
SUM(order_amount) OVER (PARTITION BY customer_id) AS percent_contribution
FROM orders;
```

---

2️⃣4️⃣ Top 3 customers by revenue
```sql
SELECT customer_id, SUM(order_amount) AS revenue
FROM orders
GROUP BY customer_id
ORDER BY revenue DESC
LIMIT 3;
```

---

2️⃣5️⃣ Customer category
```sql
SELECT customer_id,
CASE
  WHEN SUM(order_amount) > 10000 THEN 'Platinum'
  WHEN SUM(order_amount) BETWEEN 5000 AND 10000 THEN 'Gold'
  ELSE 'Silver'
END AS category
FROM orders
GROUP BY customer_id;

```
---

2️⃣6️⃣ Index Suggestions
```sql
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_payments_order ON payments(order_id);
```

---


# 🧠 SQL  MIND-HACK CHEATSHEET 
---

## 🔑 CORE PATTERN MAP (MOST IMPORTANT)

| When you see in question… | Immediately think… | Key SQL Tool | Mental Trigger |
|--------------------------|--------------------|-------------|----------------|
| previous / next | Compare rows | LAG / LEAD | Time shift |
| consecutive days | Streak logic | ROW_NUMBER | Date − row_num |
| time gap / delay | Time difference | DATEDIFF / TIMESTAMPDIFF | Lag + diff |
| session / inactivity | New session flag | Lag + CASE + SUM | Breakpoint |
| top N per group | Ranking | RANK / ROW_NUMBER | Partition |
| retention / churn | Cohort analysis | Month diff | Signup anchor |
| funnel / drop-off | Event pivot | MAX(CASE WHEN…) | NULL check |
| spike / anomaly | Compare periods | LAG + % change | Threshold |
| repeat users | Frequency | COUNT(*) > 1 | Loyalty |
| running total | Accumulation | SUM() OVER() | Cumulative |

---

## ⏱️ TIME-BASED PROBLEMS (≈50% of interviews)

| Question phrase | Correct mental model |
|-----------------|----------------------|
| days between orders | LAG(order_date) |
| inactive for 30 days | DATEDIFF(today, last_event) |
| rolling 7 days | Window frame |
| month-1 retention | TIMESTAMPDIFF(MONTH, signup, activity) |
| session after 30 mins | Gap > threshold |

---

## 🧩 WINDOW FUNCTION QUICK DECISION TABLE

| Need | Use | Why |
|-----|-----|-----|
| Previous row value | LAG() | Compare timeline |
| Next row value | LEAD() | Look ahead |
| Unique rank | ROW_NUMBER() | No ties |
| Rank with ties | RANK() | Allow ties |
| Rank without gaps | DENSE_RANK() | Continuous ranks |
| Running total | SUM() OVER() | Cumulative metric |

---

## 📊 COHORT ANALYSIS MINI-MAP

| Component | Meaning |
|----------|---------|
| cohort_month | WHO (signup batch) |
| months_since_signup | WHEN (time passed) |
| COUNT(DISTINCT user_id) | Active users |
| Retention % | Active / cohort size |

**Rule:**  
👉 Cohort analysis **ALWAYS needs 2 dimensions** (WHO + WHEN).

---

## 🔄 FUNNEL ANALYSIS CHEAT LOGIC

| Step | Pattern |
|------|---------|
| Convert events → columns | MAX(CASE WHEN …) |
| Missing step | Column is NULL |
| Drop-off detection | CASE WHEN |
| Time between steps | TIMESTAMPDIFF |

---

## ⚠️ NULL & EDGE-CASE RULES (VERY IMPORTANT)

| Situation | Correct approach |
|----------|------------------|
| AVG with NULLs | Let SQL ignore NULL |
| Only 1 event | Gap = NULL |
| COALESCE(0) | ⚠️ Use carefully |
| Multiple orders same day | Use DISTINCT if needed |

---

## 🚨 INTERVIEWER TRAPS & SAFE ANSWERS

| Trap | What you should say |
|-----|---------------------|
| Why DISTINCT? | To avoid double counting |
| Why LAG? | To compare sequence |
| What about NULLs? | Ignored intentionally |
| What if ties? | Explain rank choice |
| How to scale? | Index on date + id |

---

## 🧠 DAILY 10-MIN REVISION PLAN

| Minute | Activity |
|--------|----------|
| 1–2 | Read pattern map |
| 3–5 | Recall 2 LAG use cases |
| 6–7 | Recall 1 cohort query |
| 8–9 | Recall 1 funnel query |
| 10 | Explain logic out loud |

---
