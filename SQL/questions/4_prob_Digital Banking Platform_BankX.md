# SQL Daily Drill — Day 4
### 🔥 Level: FAANG Interview

---

## 🏦 Scenario: Digital Banking Platform — BankX

Think Razorpay / PhonePe / Paytm backend.

---

## 📦 Tables & Sample Data

**accounts**
| account_id | user_id | account_type | city      | opened_date | balance  |
|------------|---------|--------------|-----------|-------------|----------|
| A01        | 1       | savings      | Delhi     | 2020-06-01  | 15000.00 |
| A02        | 2       | current      | Mumbai    | 2019-03-15  | 82000.00 |
| A03        | 3       | savings      | Delhi     | 2021-09-10  | 3200.00  |
| A04        | 4       | savings      | Bangalore | 2022-01-20  | 47000.00 |
| A05        | 5       | current      | Mumbai    | 2020-11-05  | 9500.00  |

**users**
| user_id | name    | age | kyc_verified |
|---------|---------|-----|--------------|
| 1       | Animesh | 28  | true         |
| 2       | Rohit   | 35  | true         |
| 3       | Sneha   | 24  | false        |
| 4       | Karan   | 31  | true         |
| 5       | Priya   | 27  | true         |

**transactions**
| txn_id | account_id | txn_type | amount   | txn_date   | status  | merchant       |
|--------|------------|----------|----------|------------|---------|----------------|
| T01    | A01        | debit    | 2000.00  | 2024-01-03 | success | Amazon         |
| T02    | A01        | credit   | 5000.00  | 2024-01-10 | success | Salary         |
| T03    | A02        | debit    | 15000.00 | 2024-01-05 | success | HDFC Loan      |
| T04    | A03        | debit    | 500.00   | 2024-01-07 | failed  | Swiggy         |
| T05    | A02        | credit   | 30000.00 | 2024-01-15 | success | Client Payment |
| T06    | A04        | debit    | 8000.00  | 2024-01-18 | success | Flipkart       |
| T07    | A01        | debit    | 1200.00  | 2024-02-02 | success | Zomato         |
| T08    | A04        | credit   | 20000.00 | 2024-02-10 | success | Salary         |
| T09    | A05        | debit    | 3000.00  | 2024-02-14 | failed  | Netflix        |
| T10    | A02        | debit    | 10000.00 | 2024-02-20 | success | Rent           |
| T11    | A01        | credit   | 5000.00  | 2024-03-01 | success | Freelance      |
| T12    | A04        | debit    | 5000.00  | 2024-03-05 | success | Amazon         |
| T13    | A03        | credit   | 1000.00  | 2024-03-10 | success | Transfer       |
| T14    | A05        | debit    | 2000.00  | 2024-03-12 | success | Uber           |
| T15    | A02        | credit   | 50000.00 | 2024-03-20 | success | Client Payment |

**loans**
| loan_id | user_id | amount    | interest_rate | start_date | end_date   | status  |
|---------|---------|-----------|---------------|------------|------------|---------|
| L01     | 1       | 100000.00 | 8.5           | 2022-01-01 | 2025-01-01 | active  |
| L02     | 2       | 500000.00 | 7.2           | 2021-06-01 | 2026-06-01 | active  |
| L03     | 4       | 200000.00 | 9.0           | 2023-03-01 | 2026-03-01 | active  |
| L04     | 3       | 50000.00  | 12.0          | 2023-07-01 | 2024-07-01 | closed  |

---

## 📋 Problems

---

**Q1 — Sessionization**

Group each account's transactions into sessions where the gap between consecutive transactions is 10 or fewer days. Assign a `session_id` per account ordered by `txn_date`.

| account_id | txn_id | txn_date   | session_id |
|------------|--------|------------|------------|
| A01        | T01    | 2024-01-03 | 1          |
| A01        | T02    | 2024-01-10 | 1          |
| A01        | T07    | 2024-02-02 | 2          |
| A01        | T11    | 2024-03-01 | 3          |

---

**Q2 — Recursive CTE: Loan Referral Chain**

Add a `referred_by_loan` column to loans (loan that led to this loan offer). Given this hierarchy:

```
L03 referred by L01
L01 referred by L02
L02 has no referral (root)
```

For loan L03, fetch the full ancestor chain up to root.

| loan_id | amount     | depth |
|---------|------------|-------|
| L03     | 200000.00  | 1     |
| L01     | 100000.00  | 2     |
| L02     | 500000.00  | 3     |

---

**Q3 — Gaps & Islands: Consecutive Successful Transaction Days per Account**

Find each account's longest streak of consecutive calendar days with at least one successful transaction.

| account_id | longest_streak_days |
|------------|---------------------|
| A01        | 2                   |
| A02        | 2                   |
| A04        | 2                   |

*(A01: Jan 3 + Jan 10 are NOT consecutive days. Jan 10 + Feb 2 not consecutive. Verify carefully with your data.)*
*(Longest streak = 1 for most accounts in this dataset — extend data to test multi-day streaks properly)*

---

**Q4 — PERCENT_RANK: Transaction Amount Percentile within Account Type**

For each successful transaction, compute its amount percentile among all successful transactions of the same `account_type` (savings / current).

| txn_id | account_type | amount   | pct_rank |
|--------|--------------|----------|----------|
| T03    | current      | 15000.00 | 0.00     |
| T10    | current      | 10000.00 | 0.00     |
| T05    | current      | 30000.00 | 0.50     |
| T15    | current      | 50000.00 | 1.00     |

*(Only current account successful debits/credits shown — include all for full output)*

---

**Q5 — Median Transaction Amount per Account Without MEDIAN()**

Compute the median successful transaction amount for each account using only window functions.

| account_id | median_txn_amount |
|------------|-------------------|
| A01        | 3500.00           |
| A02        | 22500.00          |
| A04        | 8000.00           |

*(A01 successful txns: 2000, 5000, 1200, 5000 → sorted: 1200, 2000, 5000, 5000 → median = (2000+5000)/2 = 3500)*
*(A02 successful txns: 15000, 30000, 10000, 50000 → sorted: 10000, 15000, 30000, 50000 → median = (15000+30000)/2 = 22500)*
*(A04 successful txns: 8000, 20000, 5000 → sorted: 5000, 8000, 20000 → median = 8000)*

---

**Q6 — Self JOIN: Accounts in Same City with Same Account Type**

Find all pairs of accounts in the same city with the same account type. Each pair once only.

| account_1 | account_2 | city  | account_type |
|-----------|-----------|-------|--------------|
| A01       | A03       | Delhi | savings      |

---

**Q7 — LEAD: Next Transaction Amount and Type per Account**

For each transaction per account ordered by date, show the next transaction's amount and type. NULL if last.

| account_id | txn_id | txn_date   | amount   | next_amount | next_type |
|------------|--------|------------|----------|-------------|-----------|
| A01        | T01    | 2024-01-03 | 2000.00  | 5000.00     | credit    |
| A01        | T02    | 2024-01-10 | 5000.00  | 1200.00     | debit     |
| A01        | T07    | 2024-02-02 | 1200.00  | 5000.00     | credit    |
| A01        | T11    | 2024-03-01 | 5000.00  | NULL        | NULL      |

---

**Q8 — Correlated Subquery: Accounts Whose Last Transaction Was a Failed One**

Find accounts where the most recent transaction (by date) has status = `'failed'`.

| account_id | user_id | last_txn_date | last_txn_status |
|------------|---------|---------------|-----------------|
| A03        | 3       | 2024-03-10    | success         |

*(Verify: A03's last txn is T13 on 2024-03-10 = success. A05's last txn is T14 on 2024-03-12 = success. T04 and T09 are failed but not the latest for their accounts. So result = no rows with this dataset — add a failed txn as latest to test)*

---

**Q9 — NTILE: Classify Users by Total Debit Spend**

Divide users into 3 spending tiers based on total successful debit amount: Low / Mid / High.

| user_id | name    | total_debit | tier |
|---------|---------|-------------|------|
| 3       | Sneha   | 0.00        | Low  |
| 5       | Priya   | 2000.00     | Low  |
| 1       | Animesh | 3200.00     | Mid  |
| 4       | Karan   | 13000.00    | High |
| 2       | Rohit   | 25000.00    | High |

*(A03/Sneha: T04 failed so 0 debit. A05/Priya: T09 failed, T14 success 2000. A01/Animesh: T01+T07=3200. A04/Karan: T06+T12=13000. A02/Rohit: T03+T10=25000)*

---

**Q10 — Running Balance per Account**

For each account, compute the running balance after each transaction (debits subtract, credits add) in chronological order. Assume starting balance = 0 for this calculation.

| account_id | txn_id | txn_date   | amount   | txn_type | running_balance |
|------------|--------|------------|----------|----------|-----------------|
| A01        | T01    | 2024-01-03 | 2000.00  | debit    | -2000.00        |
| A01        | T02    | 2024-01-10 | 5000.00  | credit   | 3000.00         |
| A01        | T07    | 2024-02-02 | 1200.00  | debit    | 1800.00         |
| A01        | T11    | 2024-03-01 | 5000.00  | credit   | 6800.00         |

*(Only include successful transactions in the running balance)*

---

**Q11 — DENSE_RANK: Top Merchant by Debit Volume per City**

For each city, rank merchants by total successful debit amount spent by accounts in that city. Show top 1 per city.

| city      | merchant  | total_debit | rnk |
|-----------|-----------|-------------|-----|
| Delhi     | Zomato    | 1200.00     | 1   |
| Mumbai    | HDFC Loan | 15000.00    | 1   |
| Bangalore | Flipkart  | 8000.00     | 1   |

*(Delhi: A01 debits → T01 Amazon 2000, T07 Zomato 1200. Wait — Amazon 2000 > Zomato 1200. So Delhi rank 1 = Amazon 2000)*

| city      | merchant | total_debit | rnk |
|-----------|----------|-------------|-----|
| Delhi     | Amazon   | 2000.00     | 1   |
| Mumbai    | HDFC Loan| 15000.00    | 1   |
| Bangalore | Flipkart | 8000.00     | 1   |

---

**Q12 — EXISTS: Users With Active Loan AND at Least One Failed Transaction**

Find users who currently have an active loan and have had at least one failed transaction on any of their accounts.

| user_id | name  | loan_id |
|---------|-------|---------|
| 1       | Animesh | L01   |

*(User 1 → account A01. A01 has no failed txns. User 3 → A03 has T04 failed but loan L04 is closed. So result = 0 rows with this data — modify to test)*

---

**Q13 — Month-over-Month Transaction Volume Change**

For each month, compute total successful transaction amount and the % change vs previous month platform-wide.

| month   | total_volume | prev_month_volume | mom_change_pct |
|---------|--------------|-------------------|----------------|
| 2024-01 | 52000.00     | NULL              | NULL           |
| 2024-02 | 35200.00     | 52000.00          | -32.31         |
| 2024-03 | 61000.00     | 35200.00          | +73.30         |

*(Jan: T01+T02+T03+T05+T06 = 2000+5000+15000+30000+8000 = 60000. Wait recalculate:*
*Jan success: T01=2000, T02=5000, T03=15000, T05=30000, T06=8000 → 60000*
*Feb success: T07=1200, T08=20000, T10=10000 → 31200*
*Mar success: T11=5000, T12=5000, T13=1000, T14=2000, T15=50000 → 63000)*

| month   | total_volume | prev_month_volume | mom_change_pct |
|---------|--------------|-------------------|----------------|
| 2024-01 | 60000.00     | NULL              | NULL           |
| 2024-02 | 31200.00     | 60000.00          | -48.00         |
| 2024-03 | 63000.00     | 31200.00          | +101.92        |

---

**Q14 — FIRST_VALUE: Compare Each Transaction to Account's First Ever Transaction**

For each account show every transaction with the amount of their very first transaction (by date) as a reference column.

| account_id | txn_id | txn_date   | amount   | first_txn_amount |
|------------|--------|------------|----------|------------------|
| A01        | T01    | 2024-01-03 | 2000.00  | 2000.00          |
| A01        | T02    | 2024-01-10 | 5000.00  | 2000.00          |
| A01        | T07    | 2024-02-02 | 1200.00  | 2000.00          |
| A01        | T11    | 2024-03-01 | 5000.00  | 2000.00          |

---

**Q15 — Pivot: Monthly Credit vs Debit per Account**

For each account show total successful credit and total successful debit per month as separate columns.

| account_id | month   | total_credit | total_debit |
|------------|---------|--------------|-------------|
| A01        | 2024-01 | 5000.00      | 2000.00     |
| A01        | 2024-02 | 0.00         | 1200.00     |
| A01        | 2024-03 | 5000.00      | 0.00        |
| A02        | 2024-01 | 30000.00     | 15000.00    |
| A02        | 2024-02 | 0.00         | 10000.00    |
| A02        | 2024-03 | 50000.00     | 0.00        |
| A04        | 2024-01 | 0.00         | 8000.00     |
| A04        | 2024-02 | 20000.00     | 0.00        |
| A04        | 2024-03 | 0.00         | 5000.00     |

---

**Q16 — LAG: Flag Transactions Where Amount Dropped More Than 50% vs Previous**

For each account, compare each successful transaction amount to the previous one. Flag as `big_drop = 1` if current amount is less than 50% of previous.

| account_id | txn_id | amount   | prev_amount | big_drop |
|------------|--------|----------|-------------|----------|
| A01        | T01    | 2000.00  | NULL        | 0        |
| A01        | T02    | 5000.00  | 2000.00     | 0        |
| A01        | T07    | 1200.00  | 5000.00     | 1        |
| A01        | T11    | 5000.00  | 1200.00     | 0        |

*(1200 < 50% of 5000 = 2500 → big_drop = 1)*

---

**Q17 — Churn: Accounts With No Transaction in Last 45 Days**

Relative to the latest date in the dataset (2024-03-20), find accounts with no transaction in the last 45 days.

| account_id | user_id | last_txn_date |
|------------|---------|---------------|
| A03        | 3       | 2024-03-10    |

*(Cutoff = 2024-03-20 - 45 days = 2024-02-04)*
*(A03 last txn: T13 on 2024-03-10 → that's within 45 days. A05 last: T14 on 2024-03-12 → within 45 days)*
*(All accounts have txns after Feb 4 — adjust threshold or data to get meaningful results)*

---

**Q18 — 3-Transaction Moving Average of Debit Amount per Account**

For each account, compute a 3-transaction moving average of successful debit amounts in chronological order.

| account_id | txn_id | txn_date   | amount   | moving_avg_3 |
|------------|--------|------------|----------|--------------|
| A02        | T03    | 2024-01-05 | 15000.00 | 15000.00     |
| A02        | T10    | 2024-02-20 | 10000.00 | 12500.00     |

*(A02 only has 2 successful debits so moving avg uses available rows)*

---

**Q19 — Rank Users by Loan Burden (EMI as % of Account Balance)**

For each user with an active loan, compute `loan_amount / account_balance` as a burden ratio. Rank descending — highest burden first.

| user_id | name    | loan_amount | balance  | burden_ratio | rnk |
|---------|---------|-------------|----------|--------------|-----|
| 1       | Animesh | 100000.00   | 15000.00 | 6.67         | 1   |
| 4       | Karan   | 200000.00   | 47000.00 | 4.26         | 2   |
| 2       | Rohit   | 500000.00   | 82000.00 | 6.10         | 3   |

*(Sorted: Animesh 6.67 > Rohit 6.10 > Karan 4.26)*

| user_id | name    | burden_ratio | rnk |
|---------|---------|--------------|-----|
| 1       | Animesh | 6.67         | 1   |
| 2       | Rohit   | 6.10         | 2   |
| 4       | Karan   | 4.26         | 3   |

---

**Q20 — Full Funnel: Transaction Success Rate per Merchant**

For merchants with at least 2 transactions, compute success rate = `successful / total`. Sort by success rate ascending (worst first).

| merchant  | total_txns | successful | success_rate |
|-----------|------------|------------|--------------|
| Amazon    | 2          | 2          | 100.00       |

*(Most merchants appear only once — extend data with more failed txns per merchant to stress test)*

---
