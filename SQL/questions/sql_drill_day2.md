# SQL Daily Drill — Day 2
### 🔥 Level: FAANG Interview

---

## 🏢 Scenario: Ride-Sharing Platform — RideX

---

## 📦 Tables & Sample Data

**drivers**
| driver_id | name   | city      | join_date  | vehicle_type |
|-----------|--------|-----------|------------|--------------|
| 1         | Arjun  | Delhi     | 2021-05-10 | bike         |
| 2         | Mehul  | Mumbai    | 2020-11-01 | car          |
| 3         | Pooja  | Delhi     | 2022-01-15 | car          |
| 4         | Ravi   | Bangalore | 2019-08-20 | auto         |
| 5         | Simran | Mumbai    | 2023-03-05 | bike         |

**riders**
| rider_id | name    | city      | signup_date |
|----------|---------|-----------|-------------|
| 101      | Animesh | Delhi     | 2022-06-01  |
| 102      | Priya   | Mumbai    | 2021-09-15  |
| 103      | Dev     | Delhi     | 2023-01-10  |
| 104      | Aisha   | Bangalore | 2020-04-22  |

**trips**
| trip_id | driver_id | rider_id | start_time          | end_time            | status    | fare   | distance_km |
|---------|-----------|----------|---------------------|---------------------|-----------|--------|-------------|
| 1001    | 1         | 101      | 2024-01-05 08:00:00 | 2024-01-05 08:30:00 | completed | 120.00 | 8.5         |
| 1002    | 2         | 102      | 2024-01-05 09:00:00 | 2024-01-05 09:45:00 | completed | 210.00 | 15.2        |
| 1003    | 1         | 103      | 2024-01-06 10:00:00 | 2024-01-06 10:20:00 | cancelled | 0.00   | 0.0         |
| 1004    | 3         | 101      | 2024-01-07 07:30:00 | 2024-01-07 08:00:00 | completed | 95.00  | 6.0         |
| 1005    | 2         | 104      | 2024-01-08 11:00:00 | 2024-01-08 11:50:00 | completed | 340.00 | 22.1        |
| 1006    | 4         | 102      | 2024-01-09 06:00:00 | 2024-01-09 06:25:00 | completed | 80.00  | 5.5         |
| 1007    | 1         | 101      | 2024-02-01 08:00:00 | 2024-02-01 08:40:00 | completed | 150.00 | 10.0        |
| 1008    | 5         | 103      | 2024-02-03 17:00:00 | 2024-02-03 17:30:00 | cancelled | 0.00   | 0.0         |
| 1009    | 3         | 104      | 2024-02-10 09:00:00 | 2024-02-10 09:55:00 | completed | 275.00 | 18.3        |
| 1010    | 2         | 101      | 2024-03-01 08:00:00 | 2024-03-01 09:00:00 | completed | 420.00 | 30.0        |

**ratings**
| rating_id | trip_id | rated_by | score |
|-----------|---------|----------|-------|
| 1         | 1001    | rider    | 5     |
| 2         | 1001    | driver   | 4     |
| 3         | 1002    | rider    | 3     |
| 4         | 1002    | driver   | 5     |
| 5         | 1004    | rider    | 4     |
| 6         | 1005    | rider    | 5     |
| 7         | 1006    | rider    | 2     |
| 8         | 1007    | rider    | 5     |
| 9         | 1009    | rider    | 4     |
| 10        | 1010    | rider    | 3     |

---

## 📋 Problems

---

**Q1 — GROUP BY + HAVING**

Find drivers who completed more than 2 trips AND have average fare per completed trip > ₹150. Show driver name, total completed trips, avg fare.

| name  | completed_trips | avg_fare |
|-------|-----------------|----------|
| Mehul | 3               | 323.33   |

---

**Q2 — Cancellation Rate per Driver**

For each driver with at least 2 total trips, compute cancellation rate = `cancelled / total`. Sort by rate descending.

| driver_id | name  | total_trips | cancelled | cancellation_rate |
|-----------|-------|-------------|-----------|-------------------|
| 1         | Arjun | 3           | 1         | 0.33              |
| 2         | Mehul | 3           | 0         | 0.00              |

---

**Q3 — LAG: Consecutive Cancellation Flag**

For each driver, list trips chronologically. Flag `is_consecutive_cancel = 1` if both current AND previous trip were cancelled.

| driver_id | trip_id | status    | prev_status | is_consecutive_cancel |
|-----------|---------|-----------|-------------|------------------------|
| 1         | 1001    | completed | NULL        | 0                      |
| 1         | 1003    | cancelled | completed   | 0                      |
| 1         | 1007    | completed | cancelled   | 0                      |

---

**Q4 — Cumulative Earnings + 3-Trip Moving Average**

For each driver, show each completed trip with cumulative earnings so far and a 3-trip moving average of fare.

| driver_id | trip_id | fare   | cumulative_earning | moving_avg_3 |
|-----------|---------|--------|--------------------|--------------|
| 2         | 1002    | 210.00 | 210.00             | 210.00       |
| 2         | 1005    | 340.00 | 550.00             | 275.00       |
| 2         | 1010    | 420.00 | 970.00             | 323.33       |

---

**Q5 — FIRST_VALUE / LAST_VALUE**

For each rider, show all trips with two extra columns: fare of their very first trip and fare of their most recent trip.

| rider_id | trip_id | fare   | first_trip_fare | latest_trip_fare |
|----------|---------|--------|-----------------|------------------|
| 101      | 1001    | 120.00 | 120.00          | 420.00           |
| 101      | 1004    | 95.00  | 120.00          | 420.00           |
| 101      | 1007    | 150.00 | 120.00          | 420.00           |
| 101      | 1010    | 420.00 | 120.00          | 420.00           |

---

**Q6 — NTILE: Driver Earning Tiers**

Divide all drivers into 3 tiers by total completed fare: Low / Mid / High.

| driver_id | name   | total_earning | tier |
|-----------|--------|---------------|------|
| 5         | Simran | 0.00          | Low  |
| 4         | Ravi   | 80.00         | Low  |
| 1         | Arjun  | 270.00        | Mid  |
| 3         | Pooja  | 370.00        | High |
| 2         | Mehul  | 970.00        | High |

---

**Q7 — Recursive CTE: Trip Sequence per Rider**

For each rider, assign a sequence number to their trips in chronological order using a recursive CTE.

| rider_id | trip_sequence | trip_id | fare   |
|----------|---------------|---------|--------|
| 101      | 1             | 1001    | 120.00 |
| 101      | 2             | 1004    | 95.00  |
| 101      | 3             | 1007    | 150.00 |
| 101      | 4             | 1010    | 420.00 |

---

**Q8 — Gaps & Islands: Longest Active Streak per Driver**

A driver is "active" on a date if they had at least one completed trip. Find each driver's longest streak of consecutive active days.

| driver_id | name  | longest_streak_days |
|-----------|-------|---------------------|
| 2         | Mehul | 1                   |
| 1         | Arjun | 1                   |

*(Add multi-day data to fully stress-test your query)*

---

**Q9 — Rider Loyalty Label + Avg Rating Given**

Label each rider: `One-timer` (1 trip), `Regular` (2–3 trips), `Loyal` (4+ trips). Also show their average score given as a rider.

| rider_id | name    | label     | avg_rating_given |
|----------|---------|-----------|------------------|
| 101      | Animesh | Loyal     | 4.25             |
| 102      | Priya   | Regular   | 2.50             |
| 104      | Aisha   | Regular   | 4.50             |
| 103      | Dev     | One-timer | NULL             |

---

**Q10 — Self JOIN: Riders Who Shared the Same Driver**

Find all pairs of riders who were driven by the same driver at least once. Show each pair once only.

| rider_1 | rider_2 | shared_driver_id |
|---------|---------|------------------|
| 101     | 103     | 1                |
| 102     | 104     | 2                |
| 101     | 102     | 2                |

---

**Q11 — DENSE_RANK: Top Spender per City**

For each city (rider's city), rank riders by total fare spent. Show only rank 1.

| city      | rider_id | name    | total_spend | rnk |
|-----------|----------|---------|-------------|-----|
| Delhi     | 101      | Animesh | 785.00      | 1   |
| Mumbai    | 102      | Priya   | 290.00      | 1   |
| Bangalore | 104      | Aisha   | 615.00      | 1   |

---

**Q12 — EXISTS: Drivers Never Rated**

Find drivers who completed at least one trip but have never received any rating from anyone.

| driver_id | name   |
|-----------|--------|
| 5         | Simran |

---

**Q13 — CASE WHEN Pivot: Trips per Vehicle Type per Month**

Show count of completed trips for each vehicle type as separate columns, grouped by month.

| month   | bike | car | auto |
|---------|------|-----|------|
| 2024-01 | 1    | 3   | 1    |
| 2024-02 | 0    | 2   | 0    |
| 2024-03 | 0    | 1   | 0    |

---

**Q14 — Sessionization (Classic FAANG)**

Group a rider's trips into sessions. A new session starts if the gap between consecutive trips is more than 7 days. Assign a session_id per rider.

| rider_id | trip_id | start_time          | session_id |
|----------|---------|---------------------|------------|
| 101      | 1001    | 2024-01-05 08:00:00 | 1          |
| 101      | 1004    | 2024-01-07 07:30:00 | 1          |
| 101      | 1007    | 2024-02-01 08:00:00 | 2          |
| 101      | 1010    | 2024-03-01 08:00:00 | 3          |

---

**Q15 — PERCENT_RANK: Outlier Fare Detection**

For each driver's city, compute each completed trip's fare percentile within that city. Flag top 10% as `outlier`, rest as `normal`.

| trip_id | driver_city | fare   | pct_rank | fare_label |
|---------|-------------|--------|----------|------------|
| 1010    | Mumbai      | 420.00 | 1.0      | outlier    |
| 1005    | Mumbai      | 340.00 | 0.5      | normal     |
| 1002    | Mumbai      | 210.00 | 0.0      | normal     |

---

**Q16 — 7-Day Rolling Revenue + Peak Day Flag**

Compute daily platform revenue and a 7-day rolling sum. Flag the single day with highest revenue as `peak`.

| date       | daily_revenue | rolling_7day | is_peak |
|------------|---------------|--------------|---------|
| 2024-01-05 | 330.00        | 330.00       | no      |
| 2024-01-07 | 95.00         | 425.00       | no      |
| 2024-03-01 | 420.00        | 420.00       | yes     |

---

**Q17 — Median Fare Without MEDIAN Function**

Compute median fare of completed trips per driver using only window functions. No built-in MEDIAN allowed.

| driver_id | name  | median_fare |
|-----------|-------|-------------|
| 1         | Arjun | 135.00      |
| 2         | Mehul | 340.00      |
| 3         | Pooja | 185.00      |

---

**Q18 — Churn Detection**

A rider is churned if their last trip was more than 60 days before the latest date in the dataset. List churned riders.

| rider_id | name  | last_trip_date |
|----------|-------|----------------|
| 102      | Priya | 2024-01-09     |
| 103      | Dev   | 2024-02-03     |

---

**Q19 — Driver Efficiency: Fare per KM Ranked within Vehicle Type**

For each driver, compute `avg_fare_per_km` on completed trips. Rank within vehicle type.

| vehicle_type | driver_id | name  | avg_fare_per_km | rnk |
|--------------|-----------|-------|-----------------|-----|
| car          | 3         | Pooja | 15.58           | 1   |
| car          | 2         | Mehul | 14.63           | 2   |
| bike         | 1         | Arjun | 14.12           | 1   |
| auto         | 4         | Ravi  | 14.55           | 1   |

---

**Q20 — Full Funnel Conversion by City**

For each city (driver's city), compute total trips, completed, cancelled, completion %, cancellation %.

| city      | total | completed | cancelled | completion_pct | cancellation_pct |
|-----------|-------|-----------|-----------|----------------|------------------|
| Delhi     | 4     | 3         | 1         | 75.00          | 25.00            |
| Mumbai    | 4     | 3         | 1         | 75.00          | 25.00            |
| Bangalore | 1     | 1         | 0         | 100.00         | 0.00             |

---
