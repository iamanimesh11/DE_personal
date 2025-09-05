✅ Question: Find Large Attendance Streaks in a Stadium

🧠 Scenario:
You are analyzing stadium attendance. You want to identify streaks of days where the stadium had a large number of visitors. For this analysis:

* A “large attendance” day is when people ≥ 100.
* Consecutive days with large attendance are considered part of the same streak.

📂 Table: `Stadium`

```sql
CREATE TABLE Stadium (
    id INT PRIMARY KEY,
    visit_date DATE NOT NULL,
    people INT NOT NULL
);

INSERT INTO Stadium (id, visit_date, people) VALUES
(1, '2017-01-01', 10),
(2, '2017-01-02', 109),
(3, '2017-01-03', 150),
(4, '2017-01-04', 99),
(5, '2017-01-05', 145),
(6, '2017-01-06', 1455),
(7, '2017-01-07', 199),
(8, '2017-01-09', 188);
```

🎯 Task:
Write a SQL query to return all days that are part of large attendance streaks:

1. Mark each day as “large attendance” if `people >= 100`.
2. Identify consecutive days with large attendance as a streak.
3. Return all rows that are part of a streak.

💡 Expected Output (example subset):

| id | visit\_date | people |
| -- | ----------- | ------ |
| 2  | 2017-01-02  | 109    |
| 3  | 2017-01-03  | 150    |
| 5  | 2017-01-05  | 145    |
| 6  | 2017-01-06  | 1455   |
| 7  | 2017-01-07  | 199    |
| 8  | 2017-01-09  | 188    |

-- Flag large attendance days and identify streaks
WITH flagged AS (
    SELECT *,
           CASE WHEN people >= 100 THEN 1 ELSE 0 END AS is_large
    FROM Stadium
),
grouped AS (
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY id) 
           - ROW_NUMBER() OVER (PARTITION BY is_large ORDER BY id) AS grp
    FROM flagged
),
filtered AS (
    -- Keep only large attendance days
    SELECT *
    FROM grouped
    WHERE is_large = 1
)
SELECT id, visit_date, people
FROM filtered
ORDER BY id;
