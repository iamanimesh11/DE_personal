CREATE TABLE drivers (
    driver_id INT PRIMARY KEY,
    name VARCHAR(50),
    city VARCHAR(50),
    join_date DATE,
    vehicle_type VARCHAR(20)
);

INSERT INTO drivers VALUES
(1, 'Arjun', 'Delhi', '2021-05-10', 'bike'),
(2, 'Mehul', 'Mumbai', '2020-11-01', 'car'),
(3, 'Pooja', 'Delhi', '2022-01-15', 'car'),
(4, 'Ravi', 'Bangalore', '2019-08-20', 'auto'),
(5, 'Simran', 'Mumbai', '2023-03-05', 'bike');
CREATE TABLE riders (
    rider_id INT PRIMARY KEY,
    name VARCHAR(50),
    city VARCHAR(50),
    signup_date DATE
);

INSERT INTO riders VALUES
(101, 'Animesh', 'Delhi', '2022-06-01'),
(102, 'Priya', 'Mumbai', '2021-09-15'),
(103, 'Dev', 'Delhi', '2023-01-10'),
(104, 'Aisha', 'Bangalore', '2020-04-22');
CREATE TABLE trips (
    trip_id INT PRIMARY KEY,
    driver_id INT,
    rider_id INT,
    start_time DATETIME,
    end_time DATETIME,
    status VARCHAR(20),
    fare DECIMAL(10, 2),
    distance_km DECIMAL(5, 2),
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id),
    FOREIGN KEY (rider_id) REFERENCES riders(rider_id)
);

INSERT INTO trips VALUES
(1001, 1, 101, '2024-01-05 08:00:00', '2024-01-05 08:30:00', 'completed', 120.00, 8.5),
(1002, 2, 102, '2024-01-05 09:00:00', '2024-01-05 09:45:00', 'completed', 210.00, 15.2),
(1003, 1, 103, '2024-01-06 10:00:00', '2024-01-06 10:20:00', 'cancelled', 0.00, 0.0),
(1004, 3, 101, '2024-01-07 07:30:00', '2024-01-07 08:00:00', 'completed', 95.00, 6.0),
(1005, 2, 104, '2024-01-08 11:00:00', '2024-01-08 11:50:00', 'completed', 340.00, 22.1),
(1006, 4, 102, '2024-01-09 06:00:00', '2024-01-09 06:25:00', 'completed', 80.00, 5.5),
(1007, 1, 101, '2024-02-01 08:00:00', '2024-02-01 08:40:00', 'cancelled', 150.00, 10.0),
(1008, 5, 103, '2024-02-03 17:00:00', '2024-02-03 17:30:00', 'cancelled', 0.00, 0.0),
(1009, 3, 104, '2024-02-10 09:00:00', '2024-02-10 09:55:00', 'completed', 275.00, 18.3),
(1010, 2, 101, '2024-03-01 08:00:00', '2024-03-01 09:00:00', 'completed', 420.00, 30.0);

CREATE TABLE ratings (
    rating_id INT PRIMARY KEY,
    trip_id INT,
    rated_by VARCHAR(10),
    score INT,
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
);

INSERT INTO ratings VALUES
(1, 1001, 'rider', 5),(2, 1001, 'driver', 4),(3, 1002, 'rider', 3),(4, 1002, 'driver', 5),
(5, 1004, 'rider', 4),(6, 1005, 'rider', 5),(7, 1006, 'rider', 2),(8, 1007, 'rider', 5),
(9, 1009, 'rider', 4),(10, 1010, 'rider', 3);

-- =========================
-- Q1 — GROUP BY + HAVING
-- =========================
SELECT d.name,
       COUNT(*) AS completed_trips,
       AVG(t.fare) AS avg_fare
FROM trips t
JOIN drivers d ON d.driver_id = t.driver_id
WHERE t.status = 'completed'
GROUP BY d.driver_id, d.name
HAVING COUNT(*) > 2 AND AVG(t.fare) > 150;


-- =========================
-- Q2 — Cancellation Rate
-- =========================
SELECT d.driver_id,
       d.name,
       COUNT(*) AS total_trips,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
       ROUND(SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 2) AS cancellation_rate
FROM trips t
JOIN drivers d ON d.driver_id = t.driver_id
GROUP BY d.driver_id, d.name
HAVING COUNT(*) >= 2
ORDER BY cancellation_rate DESC;


-- =========================
-- Q3 — LAG
-- =========================
SELECT driver_id,
       trip_id,
       status,
       LAG(status) OVER (PARTITION BY driver_id ORDER BY start_time) AS prev_status,
       CASE 
           WHEN status = 'cancelled' 
            AND LAG(status) OVER (PARTITION BY driver_id ORDER BY start_time) = 'cancelled'
           THEN 1 ELSE 0
       END AS is_consecutive_cancel
FROM trips;


-- =========================
-- Q4 — Cumulative + Moving Avg
-- =========================
SELECT driver_id,
       trip_id,
       fare,
       SUM(fare) OVER (PARTITION BY driver_id ORDER BY start_time) AS cumulative_earning,
       AVG(fare) OVER (
           PARTITION BY driver_id 
           ORDER BY start_time
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS moving_avg_3
FROM trips
WHERE status = 'completed';


-- =========================
-- Q5 — FIRST_VALUE / LAST_VALUE
-- =========================
SELECT rider_id,
       trip_id,
       fare,
       FIRST_VALUE(fare) OVER (PARTITION BY rider_id ORDER BY start_time) AS first_trip_fare,
       LAST_VALUE(fare) OVER (
           PARTITION BY rider_id 
           ORDER BY start_time 
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS latest_trip_fare
FROM trips
WHERE status = 'completed';


-- =========================
-- Q6 — NTILE
-- =========================
WITH earnings AS (
    SELECT d.driver_id,
           d.name,
           COALESCE(SUM(t.fare), 0) AS total_earning
    FROM drivers d
    LEFT JOIN trips t 
        ON d.driver_id = t.driver_id AND t.status = 'completed'
    GROUP BY d.driver_id, d.name
)
SELECT *,
       CASE NTILE(3) OVER (ORDER BY total_earning)
            WHEN 1 THEN 'Low'
            WHEN 2 THEN 'Mid'
            ELSE 'High'
       END AS tier
FROM earnings;


-- =========================
-- Q7 — Recursive CTE
-- =========================
WITH RECURSIVE ordered AS (
    SELECT rider_id, trip_id, fare, start_time,
           ROW_NUMBER() OVER (PARTITION BY rider_id ORDER BY start_time) AS rn
    FROM trips
),
cte AS (
    SELECT rider_id, trip_id, fare, rn AS trip_sequence
    FROM ordered
    WHERE rn = 1
    UNION ALL
    SELECT o.rider_id, o.trip_id, o.fare, c.trip_sequence + 1
    FROM cte c
    JOIN ordered o 
      ON c.rider_id = o.rider_id 
     AND o.rn = c.trip_sequence + 1
)
SELECT * FROM cte;


-- =========================
-- Q8 — Gaps & Islands
-- =========================
WITH distinct_days AS (
    SELECT DISTINCT driver_id, DATE(start_time) AS trip_date
    FROM trips
    WHERE status = 'completed'
),
grp AS (
    SELECT driver_id,
           trip_date,
           DATE_SUB(trip_date, INTERVAL ROW_NUMBER() OVER (PARTITION BY driver_id ORDER BY trip_date) DAY) AS grp
    FROM distinct_days
)
SELECT driver_id,
       COUNT(*) AS longest_streak_days
FROM grp
GROUP BY driver_id, grp
ORDER BY longest_streak_days DESC;


-- =========================
-- Q9 — Loyalty + Avg Rating
-- =========================
WITH trip_counts AS (
    SELECT rider_id, COUNT(*) AS total_trips
    FROM trips
    GROUP BY rider_id
),
ratings_cte AS (
    SELECT t.rider_id, AVG(r.score) AS avg_rating
    FROM ratings r
    JOIN trips t ON r.trip_id = t.trip_id
    WHERE r.rated_by = 'rider'
    GROUP BY t.rider_id
)
SELECT r.rider_id,
       r.name,
       CASE 
           WHEN t.total_trips = 1 THEN 'One-timer'
           WHEN t.total_trips BETWEEN 2 AND 3 THEN 'Regular'
           ELSE 'Loyal'
       END AS label,
       rc.avg_rating
FROM riders r
LEFT JOIN trip_counts t ON r.rider_id = t.rider_id
LEFT JOIN ratings_cte rc ON r.rider_id = rc.rider_id;


-- =========================
-- Q10 — Self Join
-- =========================
SELECT DISTINCT
    t1.rider_id AS rider_1,
    t2.rider_id AS rider_2,
    t1.driver_id
FROM trips t1
JOIN trips t2 
  ON t1.driver_id = t2.driver_id
WHERE t1.rider_id < t2.rider_id;


-- =========================
-- Q11 — DENSE_RANK
-- =========================
WITH spend AS (
    SELECT r.city, r.rider_id, r.name, SUM(t.fare) AS total_spend
    FROM riders r
    JOIN trips t ON r.rider_id = t.rider_id
    GROUP BY r.city, r.rider_id, r.name
)
SELECT *,
       DENSE_RANK() OVER (PARTITION BY city ORDER BY total_spend DESC) AS rnk
FROM spend
WHERE total_spend IS NOT NULL;


-- =========================
-- Q12 — EXISTS
-- =========================
SELECT d.driver_id, d.name
FROM drivers d
WHERE EXISTS (
    SELECT 1 FROM trips t
    WHERE t.driver_id = d.driver_id AND t.status = 'completed'
)
AND NOT EXISTS (
    SELECT 1 
    FROM ratings r
    JOIN trips t ON r.trip_id = t.trip_id
    WHERE t.driver_id = d.driver_id
);


-- =========================
-- Q13 — Pivot
-- =========================
SELECT DATE_FORMAT(start_time, '%Y-%m') AS month,
       SUM(CASE WHEN d.vehicle_type = 'bike' THEN 1 ELSE 0 END) AS bike,
       SUM(CASE WHEN d.vehicle_type = 'car' THEN 1 ELSE 0 END) AS car,
       SUM(CASE WHEN d.vehicle_type = 'auto' THEN 1 ELSE 0 END) AS auto
FROM trips t
JOIN drivers d ON t.driver_id = d.driver_id
WHERE t.status = 'completed'
GROUP BY month;


-- =========================
-- Q14 — Sessionization
-- =========================
WITH cte AS (
    SELECT *,
           CASE 
               WHEN TIMESTAMPDIFF(DAY,
                    LAG(start_time) OVER (PARTITION BY rider_id ORDER BY start_time),
                    start_time) > 7
               THEN 1 ELSE 0
           END AS new_session
    FROM trips
),
sessionized AS (
    SELECT *,
           SUM(new_session) OVER (PARTITION BY rider_id ORDER BY start_time) + 1 AS session_id
    FROM cte
)
SELECT rider_id, trip_id, start_time, session_id
FROM sessionized;


-- =========================
-- Q15 — Percent Rank
-- =========================
SELECT t.trip_id,
       d.city,
       t.fare,
       PERCENT_RANK() OVER (PARTITION BY d.city ORDER BY t.fare) AS pct_rank,
       CASE 
           WHEN PERCENT_RANK() OVER (PARTITION BY d.city ORDER BY t.fare) >= 0.9 
           THEN 'outlier'
           ELSE 'normal'
       END AS label
FROM trips t
JOIN drivers d ON t.driver_id = d.driver_id
WHERE t.status = 'completed';


-- =========================
-- Q16 — Rolling Revenue
-- =========================
WITH daily AS (
    SELECT DATE(start_time) AS dt,
           SUM(fare) AS daily_revenue
    FROM trips
    WHERE status = 'completed'
    GROUP BY dt
)
SELECT *,
       SUM(daily_revenue) OVER (
           ORDER BY dt 
           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ) AS rolling_7day,
       CASE 
           WHEN daily_revenue = MAX(daily_revenue) OVER ()
           THEN 'yes' ELSE 'no'
       END AS is_peak
FROM daily;


-- =========================
-- Q17 — Median
-- =========================
WITH ranked AS (
    SELECT d.driver_id, d.name, t.fare,
           ROW_NUMBER() OVER (PARTITION BY d.driver_id ORDER BY t.fare) AS rn,
           COUNT(*) OVER (PARTITION BY d.driver_id) AS cnt
    FROM trips t
    JOIN drivers d ON t.driver_id = d.driver_id
    WHERE status = 'completed'
)
SELECT driver_id, name,
       AVG(fare) AS median_fare
FROM ranked
WHERE rn IN (FLOOR((cnt+1)/2), FLOOR((cnt+2)/2))
GROUP BY driver_id, name;


-- =========================
-- Q18 — Churn
-- =========================
WITH last_trip AS (
    SELECT rider_id,
           MAX(start_time) AS last_trip,
           MAX(MAX(start_time)) OVER () AS max_date
    FROM trips
    GROUP BY rider_id
)
SELECT r.rider_id, r.name, last_trip
FROM last_trip lt
JOIN riders r ON lt.rider_id = r.rider_id
WHERE DATEDIFF(max_date, last_trip) > 60;


-- =========================
-- Q19 — Efficiency
-- =========================
WITH calc AS (
    SELECT driver_id,
           SUM(fare) / SUM(distance_km) AS avg_fare_per_km
    FROM trips
    WHERE status = 'completed'
    GROUP BY driver_id
)
SELECT d.vehicle_type,
       d.driver_id,
       d.name,
       ROUND(c.avg_fare_per_km, 2),
       RANK() OVER (PARTITION BY d.vehicle_type ORDER BY c.avg_fare_per_km DESC) AS rnk
FROM calc c
JOIN drivers d ON d.driver_id = c.driver_id;


-- =========================
-- Q20 — Funnel
-- =========================
SELECT d.city,
       COUNT(*) AS total,
       SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
       ROUND(SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END)*100.0/COUNT(*),2) AS completion_pct,
       ROUND(SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)*100.0/COUNT(*),2) AS cancellation_pct
FROM trips t
JOIN drivers d ON d.driver_id = t.driver_id
GROUP BY d.city;
