✅ Question 1 :
"Write a SQL query to find, for each customer, the product they have purchased the most frequently (only considering products bought more than twice). If there are ties, return all top products for that customer."

💡 Solution: 
with cte as(
select count(customer_id) as product_bought_often ,customer_id,
        product_name
      from customer_orders 
      group by product_name ,customer_id
      having product_bought_often >2
      )
,
cte2 as ( select product_bought_often,customer_id,product_name,
rank() over ( partition by customer_id  order by product_bought_often desc) as rn
from cte)

select  from cte2
where rn=1


✅ Question 2: User Logins & Retention

Base Table

```sql
CREATE TABLE user_logins (
    login_id INT PRIMARY KEY,    user_id VARCHAR(50),login_date DATE );

INSERT INTO user_logins (login_id, user_id, login_date) VALUES
(1, 'U1', '2024-06-01'),(2, 'U1', '2024-06-02'),(3, 'U1', '2024-06-03'),(4, 'U1', '2024-06-04'),(5, 'U1', '2024-06-05'),(6, 'U1', '2024-06-06'),(7, 'U1', '2024-06-07'),(8, 'U2', '2024-06-01'),(9, 'U2', '2024-06-03'),(10, 'U3', '2024-06-10'),(11, 'U3', '2024-06-11'),(12, 'U3', '2024-06-12'),(13, 'U3', '2024-06-13'),(14, 'U3', '2024-06-14'),(15, 'U3', '2024-06-15'),(16, 'U3', '2024-06-16');
```

✅ Question 2.1: Longest login streak per user

Problem: Find the maximum consecutive login days for each user.

💡Answer:

```sql
WITH base AS (
    SELECT user_id, login_date,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM user_logins
),
streaks AS (
    SELECT user_id, login_date, login_date - INTERVAL rn DAY AS streak_base
    FROM base
),
streak_lengths AS (
    SELECT user_id, COUNT() AS streak_length
    FROM streaks
    GROUP BY user_id, streak_base
)
SELECT user_id, MAX(streak_length) AS longest_streak
FROM streak_lengths
GROUP BY user_id;
```

Explanation: Assigns row numbers to identify consecutive dates; grouping by `streak_base` calculates streak lengths.


✅ Question 2.2: Start date of first 7-day streak

Problem: Find the start date of the first 7-day streak per user.

💡Answer:
```sql
WITH base AS (
    SELECT user_id, login_date,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM user_logins
),
streaks AS (
    SELECT user_id, login_date, login_date - INTERVAL rn DAY AS streak_base
    FROM base
),
streak_groups AS (
    SELECT user_id, streak_base, COUNT() AS streak_length, MIN(login_date) AS streak_start
    FROM streaks
    GROUP BY user_id, streak_base
    HAVING COUNT() >= 7
)
SELECT user_id, MIN(streak_start) AS first_7_day_streak_start
FROM streak_groups
GROUP BY user_id;
```


✅ Question 2.3: Count of 7-day streaks per user

Problem: Count how many streaks of 7 or more days each user has.

💡Answer:

```sql
WITH base AS (
    SELECT user_id, login_date,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM user_logins
),
streaks AS (
    SELECT user_id, login_date, login_date - INTERVAL rn DAY AS streak_base
    FROM base
),
streak_groups AS (
    SELECT user_id, streak_base, COUNT() AS streak_length
    FROM streaks
    GROUP BY user_id, streak_base
    HAVING COUNT() >= 7
)
SELECT user_id, COUNT() AS number_of_7_day_streaks
FROM streak_groups
GROUP BY user_id;
```

---

✅ Question 2.4: Average streak length per user

Problem: Calculate the average streak length for each user.

💡Answer:

```sql
WITH base AS (
    SELECT user_id, login_date,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM user_logins
),
streaks AS (
    SELECT user_id, login_date, login_date - INTERVAL rn DAY AS streak_base
    FROM base
),
streak_groups AS (
    SELECT user_id, streak_base, COUNT() AS streak_length
    FROM streaks
    GROUP BY user_id, streak_base
)
SELECT user_id, ROUND(AVG(streak_length), 2) AS avg_streak_length
FROM streak_groups
GROUP BY user_id;
```


✅ Question 2.5: Gap between top 2 streaks

Problem: Find the number of days between the longest streak end and the second-longest streak start.

💡Answer:

```sql
WITH streaks AS (
    SELECT user_id, login_date,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM user_logins
),
streak_base AS (
    SELECT user_id, login_date, login_date - INTERVAL rn DAY AS base
    FROM streaks
),
streak_lengths AS (
    SELECT user_id, base, COUNT() AS streak_len, MIN(login_date) AS start_date, MAX(login_date) AS end_date
    FROM streak_base
    GROUP BY user_id, base
),
ranked AS (
    SELECT , RANK() OVER (PARTITION BY user_id ORDER BY streak_len DESC) AS rnk
    FROM streak_lengths
)
SELECT user_id,
       MAX(CASE WHEN rnk = 1 THEN end_date END) AS longest_end,
       MAX(CASE WHEN rnk = 2 THEN start_date END) AS second_start,
       DATEDIFF(MAX(CASE WHEN rnk = 2 THEN start_date END), MAX(CASE WHEN rnk = 1 THEN end_date END)) AS gap_days
FROM ranked
GROUP BY user_id
HAVING COUNT() >= 2;
```

---

✅ Question 2.6: Users who dropped off after 7-day streak

Problem: Identify users who had a streak of ≥7 days and did not log in for the next 3 days.

💡Answer:

```sql
WITH streaks AS (
    SELECT user_id, login_date,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM user_logins
),
streak_base AS (
    SELECT user_id, login_date, login_date - INTERVAL rn DAY AS base
    FROM streaks
),
user_streaks AS (
    SELECT user_id, base, COUNT() AS streak_len, MAX(login_date) AS streak_end
    FROM streak_base
    GROUP BY user_id, base
    HAVING COUNT() >= 7
),
next_logins AS (
    SELECT s.user_id, s.streak_end, MIN(l.login_date) AS next_login
    FROM user_streaks s
    LEFT JOIN user_logins l 
        ON s.user_id = l.user_id AND l.login_date > s.streak_end
    GROUP BY s.user_id, s.streak_end
)
SELECT user_id, streak_end, next_login, DATEDIFF(next_login, streak_end) AS gap_days
FROM next_logins
WHERE next_login IS NULL OR DATEDIFF(next_login, streak_end) > 3;
```

---

✅ Question 2.7: Day 1, Day 3, Day 7 Retention

Problem: For each signup date, calculate the percentage of users returning on day 1, 3, and 7.

Assume a table:

```sql
signups(user_id, signup_date)
```

💡Answer:

```sql
SELECT s.signup_date,
       ROUND(SUM(u.login_day = 1) / COUNT(), 2) AS day1_retention,
       ROUND(SUM(u.login_day = 3) / COUNT(), 2) AS day3_retention,
       ROUND(SUM(u.login_day = 7) / COUNT(), 2) AS day7_retention
FROM signups s
LEFT JOIN (
    SELECT l.user_id, DATEDIFF(l.login_date, s.signup_date) AS login_day
    FROM user_logins l
    JOIN signups s ON l.user_id = s.user_id
) u ON s.user_id = u.user_id
GROUP BY s.signup_date;
```

---

✅ Question 2.8: Segment users by behavior tier

Problem: Classify users into tiers based on maximum streak:

 `Addicted` ≥7 days
 `Engaged` 3–6 days
 `Casual` <3 days

💡Answer:

```sql
WITH user_streaks AS (
    SELECT user_id, COUNT() AS streak_length
    FROM (
        SELECT user_id, login_date,
               ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
        FROM user_logins
    ) base
    GROUP BY user_id, login_date - INTERVAL rn DAY
),
max_streaks AS (
    SELECT user_id, MAX(streak_length) AS max_streak
    FROM user_streaks
    GROUP BY user_id
)
SELECT user_id, max_streak,
       CASE 
           WHEN max_streak >= 7 THEN 'Addicted'
           WHEN max_streak >= 3 THEN 'Engaged'
           ELSE 'Casual'
       END AS user_tier
FROM max_streaks;
```

---

✅ Question 2.9: Calendar-style heatmap

Problem: Show whether a user logged in on each day from `2024-06-01` to `2024-06-07`.

💡Answer:

```sql
SELECT user_id,
       MAX(login_date = '2024-06-01') AS d1,
       MAX(login_date = '2024-06-02') AS d2,
       MAX(login_date = '2024-06-03') AS d3,
       MAX(login_date = '2024-06-04') AS d4,
       MAX(login_date = '2024-06-05') AS d5,
       MAX(login_date = '2024-06-06') AS d6,
       MAX(login_date = '2024-06-07') AS d7
FROM user_logins
GROUP BY user_id;
```

---

✅ Question 2.10: Users with at least one streak ≥5 days

Problem: List users who had any streak of 5 days or longer.

💡Answer:

```sql
WITH streaks AS (
    SELECT user_id, login_date,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM user_logins
),
streak_base AS (
    SELECT user_id, login_date, login_date - INTERVAL rn DAY AS base
    FROM streaks
),
streak_lengths AS (
    SELECT user_id, COUNT() AS streak_len
    FROM streak_base
    GROUP BY user_id, base
)
SELECT DISTINCT user_id
FROM streak_lengths
WHERE streak_len >= 5;
```




✅ Question 3: Business Case – Revenue Loss Due to Cart Abandonment

💼 Task: Calculate the total potential revenue lost due to cart abandonment.

📂 Table: `user_events`

| event\_id | user\_id | event\_type   | event\_time         | product\_id | price |
| --------- | -------- | ------------- | ------------------- | ----------- | ----- |
| 1         | U1       | browse        | 2024-06-01 10:00:00 | P1          | NULL  |
| 2         | U1       | add\_to\_cart | 2024-06-01 10:02:00 | P1          | 500   |
| 3         | U1       | payment       | 2024-06-01 10:10:00 | P1          | 500   |
| 4         | U2       | browse        | 2024-06-01 10:01:00 | P2          | NULL  |
| 5         | U2       | add\_to\_cart | 2024-06-01 10:05:00 | P2          | 800   |
| 6         | U3       | add\_to\_cart | 2024-06-01 11:00:00 | P3          | 1200  |
| 7         | U4       | add\_to\_cart | 2024-06-01 11:02:00 | P1          | 500   |
| 8         | U4       | payment       | 2024-06-01 11:10:00 | P1          | 500   |

💡 Hint:

* Find all `add_to_cart` actions
* Exclude any items that were later purchased (`payment`) by the same user and product
* Sum the prices of the remaining items to get lost revenue

🎯 Expected Output:

| lost\_revenue |
| ------------- |
| 2000          |

💭 Explanation:

* U2 added P2 (800) but didn’t pay
* U3 added P3 (1200) but didn’t pay

💡 SQL Solution:

```sql
SELECT SUM(a.price) AS lost_revenue
FROM user_events a
WHERE a.event_type = 'add_to_cart'
AND NOT EXISTS (
    SELECT 1
    FROM user_events p
    WHERE p.event_type = 'payment'
      AND p.user_id = a.user_id
      AND p.product_id = a.product_id
);
```

✅ Question 4:> Calculate the total potential revenue lost due to cart abandonment.

💡 SQL Solution:

CREATE TABLE user_events (
    event_id INT PRIMARY KEY,
    user_id VARCHAR(50),
    event_type VARCHAR(50),
    event_time DATETIME,
    product_id VARCHAR(50),
    price DECIMAL(10, 2)
);

INSERT INTO user_events (event_id, user_id, event_type, event_time, product_id, price) VALUES
    (1, 'U1', 'browse', '2024-06-01 10:00:00', 'P1', NULL),
    (2, 'U1', 'add_to_cart', '2024-06-01 10:02:00', 'P1', 500.00),
    (3, 'U1', 'payment', '2024-06-01 10:10:00', 'P1', 500.00),
    (4, 'U2', 'browse', '2024-06-01 10:01:00', 'P2', NULL),
    (5, 'U2', 'add_to_cart', '2024-06-01 10:05:00', 'P2', 800.00),
    (6, 'U3', 'add_to_cart', '2024-06-01 11:00:00', 'P3', 1200.00),
    (7, 'U4', 'add_to_cart', '2024-06-01 11:02:00', 'P1', 500.00),
    (8, 'U4', 'payment', '2024-06-01 11:10:00', 'P1', 500.00),
    (9, 'U5', 'add_to_cart', '2024-06-01 12:00:00', 'P4', 700.00),
    (10, 'U5', 'payment', '2024-06-02 12:10:00', 'P4', 700.00),
    (11, 'U5', 'add_to_cart', '2024-06-03 13:00:00', 'P4', 700.00),
    (12, 'U6', 'add_to_cart', '2024-06-04 09:00:00', 'P5', 600.00),
    (13, 'U6', 'add_to_cart', '2024-06-04 09:05:00', 'P6', 900.00),
    (14, 'U6', 'payment', '2024-06-04 09:10:00', 'P6', 900.00);
    
    
with add_to_cart_events AS (

select * from user_events
where event_type="add_to_cart"

)
, payment_EVENTS  as (
select distinct user_id,product_id
from user_events
where event_type='payment'

)
,
abandoned_Carts as (
select a.user_id,a.product_id,a.price
from add_to_cart_events a 
left join payment_EVENTS p 
on a.user_id=p.user_id and a.product_id=p.product_id
where p.user_id is NULL

)

-- select sum(price) from fcte

select  sum(price) as last_revenue from abandoned_Carts


✅ Question 5:> Calculate the total potential revenue lost due to cart abandonment.

🗂️ Table: user_orders
order_id	user_id	product_id	order_date	price

101	U1	P1	2024-06-01	500
102	U1	P2	2024-06-02	800
103	U1	P1	2024-06-05	500
104	U2	P3	2024-06-01	600
105	U2	P3	2024-06-04	600
106	U2	P3	2024-06-08	600
107	U3	P1	2024-06-01	500
108	U3	P4	2024-06-02	900
---
🎯 Task:
Find the top 1 most frequently bought product for each user.
If a user has multiple products with the same frequency, return any one of them.

CREATE TABLE user_orders (
    order_id INT PRIMARY KEY,
    user_id VARCHAR(50),
    product_id VARCHAR(50),
    order_date DATE,
    price DECIMAL(10, 2)
);

INSERT INTO user_orders (order_id, user_id, product_id, order_date, price) VALUES
    (101, 'U1', 'P1', '2024-06-01', 500.00),(102, 'U1', 'P2', '2024-06-02', 800.00),(103, 'U1', 'P1', '2024-06-05', 500.00),(104, 'U2', 'P3', '2024-06-01', 600.00),
    (105, 'U2', 'P3', '2024-06-04', 600.00),(106, 'U2', 'P3', '2024-06-08', 600.00),(107, 'U3', 'P1', '2024-06-01', 500.00),(108, 'U3', 'P4', '2024-06-02', 900.00);

with cte as (
select user_id,product_id,count(*) as total_orders
from user_orders
group by user_id,product_id
)
,
ranked_cte as(
select user_id,product_id,total_orders,
rank() over (partition by user_id order by total_orders desc) as rn 
from cte 
)

select * from ranked_cte
where rn=1


✅ Question 6: > Identify all duplicate orders — defined as orders from the same user, for the same product, on the same date, with the same amount.

💡 SQL Solution:
with cte as (
select user_id,product_id,count(product_id)
from orders
group by user_id,product_id,order_date,amount
having count(*)>=2
),cte2 as (

select o.user_id,o.product_id,o.order_date,o.amount
from orders o 
join cte c 
on o.user_id=c.user_id and o.product_id=c.product_id
)

select distinct user_id,product_id,order_date,amount
from cte2


✅ Question 7: >> For each product, list the date(s) where units_sold was at least 3 times the average daily sales for that product.
💡 SQL Solution: 

CREATE TABLE product_sales (
    sale_id INT PRIMARY KEY,
    product_id VARCHAR(50),
    sale_date DATE,
    units_sold INT
);

INSERT INTO product_sales (sale_id, product_id, sale_date, units_sold) VALUES
    (1, 'P1', '2024-06-01', 10),
    (2, 'P1', '2024-06-02', 12),
    (3, 'P1', '2024-06-03', 11),
    (4, 'P1', '2024-06-04', 45),
    (5, 'P2', '2024-06-01', 5),
    (6, 'P2', '2024-06-02', 4),
    (7, 'P2', '2024-06-03', 16),
    (8, 'P3', '2024-06-01', 6);
    
    
with cte as (
select 
       product_id,sale_date,units_sold,
       sum(units_sold) over (
        partition  by product_id
       ) as total_sum,
       count(*) over (partition by product_id) as total_count
    from product_sales 
  ),
spie_check as (
select product_id,
      sale_date,
      units_sold,
      round(total_sum*1.0/total_count,2) as avg_Daily_units
from cte 
)

select * from spie_check
where units_sold>=3*avg_Daily_units

✅ Question 8: >> Find products whose order count in the last 1 hour is at least 3x more than their average orders per hour in the last 24 hours.

💡 SQL Solution: 

🗂️ Table: orders

order_id	product_id	order_time
1	P1	2024-06-19 09:00:00
2	P1	2024-06-19 10:00:00
3	P1	2024-06-20 08:30:00
4	P2	2024-06-20 08:35:00
5	P1	2024-06-20 08:40:00
6	P1	2024-06-20 08:45:00


with orders_1hr as (
select product_id,
count(*) as orders_1hr
from orders where order_time>='2024-06-20 07:59:59'
group by product_id
),
orders_24hr as (
select product_id,
count(*) as orders_24hr,
count(*)/24 as avgorder_per_hour
from orders
where order_time between '2024-06-19 08:59:59' and '2024-06-20 08:59:59'
group by product_id
)
select o24.product_id ,o1.orders_1hr,o24.avgorder_per_hour,
o1.orders_1hr/o24.avgorder_per_hour as spike_Ratio,
case 
    when o1.orders_1hr>-3*o24.avgorder_per_hour then 'Spike'
    else '-'
    end as spike_flag 
from orders_24hr o24
join orders_1hr o1 
on o24.product_id=o1.product_id
where o1.orders_1hr>=3*avgorder_per_hour

Output:

+------------+------------+-------------------+-------------+------------+
| product_id | orders_1hr | avgorder_per_hour | spike_Ratio | spike_flag |
+------------+------------+-------------------+-------------+------------+
| P1         |          3 |            0.2083 |     14.4023 | Spike      |
| P2         |          1 |            0.0417 |     23.9808 | Spike      |
+------------+------------+-------------------+-------------+------------+


✅ Question 9: >> Repeated Add to Cart Within 30 Minutes

> For each user, detect if they added the same product to their cart more than once within a 30-minute window.

💡 SQL Solution: 

🗂️ Table: cart_events

user_id	product_id	event_time	event_type

U1	P1	2024-06-20 09:00:00	add_to_cart
U1	P1	2024-06-20 09:20:00	add_to_cart
U1	P1	2024-06-20 10:10:00	add_to_cart
U2	P2	2024-06-20 11:00:00	add_to_cart
U2	P2	2024-06-20 11:31:00	add_to_cart
U3	P3	2024-06-20 12:00:00	browse

with cte as (
 select * ,
lag(event_time) over (
partition by user_id,product_id
order by event_time
) as previous_add_time
 from user_events
 )
 
 select * from cte 
WHERE TIMESTAMPDIFF(MINUTE, previous_add_time, event_time) <= 30


✅ Question 10 : >> Repeated Add to Cart Within 30 Minutes

> For each user, detect if they added the same product to their cart more than once within a 30-minute window.
1. start_course  
2. complete_video  
3. quiz_start  
4. quiz_submit
📂 Table: course_events
| user\_id | event\_type     | event\_time         |
| -------- | --------------- | ------------------- |
| U1       | start\_course   | 2024-06-20 08:00:00 |
| U1       | complete\_video | 2024-06-20 08:15:00 |
| U1       | quiz\_start     | 2024-06-20 08:20:00 |
| U1       | quiz\_submit    | 2024-06-20 08:25:00 |
| U2       | start\_course   | 2024-06-20 08:30:00 |
| U2       | quiz\_start     | 2024-06-20 08:45:00 |
| U3       | complete\_video | 2024-06-20 09:00:00 |
| U3       | quiz\_start     | 2024-06-20 09:10:00 |

💡 SQL Solution: 
with arranged_event_type as (
       SELECT * ,
            row_number() over (
                  partition by user_id
                  order by field(event_type,"start_course","complete_video","quiz_start","quiz_submit")) as priority_rank ,
              lag(event_time) over(
                  partition by user_id
                  order  by event_time
                  ) as previous_Event_time,
              coalesce(timestampdiff(minute,
                                  lag(event_time) over(
                                    partition by user_id
                                    order  by event_time),event_time)
                      ,0)
                      as time_diff 
                                  from user_events
                )

,max_Avg_cte as  (
      SELECT *,
                max(priority_rank) over (
                  partition by user_id
                ) as max_Step,
                avg(time_diff) over (
                  partition by user_id) as avg_time_between_each_step
          from arranged_event_type
      )
,user_Status_cte as (
      select distinct user_id ,max_Step  ,avg_time_between_each_step
      from max_Avg_cte
      )
-- question 1 .
,user_funnel_summary as (
select 
  user_id ,
  case max_Step
    when 4 then "Completed"
    when 3 then "Dropeed after quiz_Start"
    when 2 then "stuck after complete_video"
    when 1 then "stuck after start_course"
    else 'No Progress'
    end  
    as funnel_Status ,
  case max_Step
    when 3 then "quiz_start"
    when 2 then "complete_video"
    when 1 then "start_course"
    else NULL 
    end  
    as last_Step ,
  case max_Step
    when 3 then "missing quiz_submit"
    when 2 then "missing quiz_start"
    when 1 then "missing complete_video"
    end  
    as next_missing_step,
  avg_time_between_each_step
from user_Status_cte
)

select * from user_funnel_summary 


✅ Question 11 : >> Repeated Add to Cart Within 30 Minutes

💡 SQL Solution: 
📂 Table: feature_usage

| user\_id | feature\_name   | usage\_date |
| -------- | --------------- | ----------- |
| U1       | Smart Templates | 2024-06-01  |
| U1       | Smart Templates | 2024-06-02  |
| U2       | Smart Templates | 2024-06-01  |
| U3       | Smart Templates | 2024-06-06  |
| U3       | Smart Templates | 2024-06-08  |
| U4       | Smart Templates | 2024-06-11  |
| U5       | Smart Templates | 2024-06-12  |

🎯 Task:

Return for each week:
week_start (Monday of the week)
Number of distinct users (user_count) who used "Smart Templates"
trend label:
'New Spike' → user count ≥ 50% higher than previous week
'Drop' → user count ≥ 50% lower than previous week
'Stable' → otherwise

💡 SQL Solution:

WITH weekly_usage AS (
    SELECT 
        DATE_TRUNC('week', usage_date) AS week_start,
        COUNT(DISTINCT user_id) AS user_count
    FROM feature_usage
    WHERE feature_name = 'Smart Templates'
    GROUP BY DATE_TRUNC('week', usage_date)
),
weekly_trend AS (
    SELECT
        week_start,
        user_count,
        LAG(user_count) OVER (ORDER BY week_start) AS prev_week_count
    FROM weekly_usage
)
SELECT
    week_start,
    user_count,
    CASE
        WHEN prev_week_count IS NULL THEN NULL
        WHEN user_count >= 1.5 * prev_week_count THEN 'New Spike'
        WHEN user_count <= 0.5 * prev_week_count THEN 'Drop'
        ELSE 'Stable'
    END AS trend
FROM weekly_trend
ORDER BY week_start;

✅ Question 12: Swap Adjacent Rows in a Table

swap every pair of adjacent rows based on their insertion order (id). If there’s an odd number of rows, the last row remains in place.

💡 SQL Solution:
-- Create the students table
CREATE TABLE nums (
    id INT PRIMARY KEY AUTO_INCREMENT, -- id as the primary key, auto-incremented
    val VARCHAR(255) NOT NULL -- student name (variable length string, not null)
);

-- Insert sample data
INSERT INTO nums (val) VALUES
('Alice'),('Bob'),('Charlie'),('David'),('Eve'),('FISH');

WITH numbered AS (
  SELECT
    id,
    val,
    ROW_NUMBER() OVER (ORDER BY id) AS rn
  FROM nums
),
odd_rows AS (
  SELECT rn, id, val FROM numbered WHERE MOD(rn, 2) = 1
),
even_rows AS (
  SELECT rn, id, val FROM numbered WHERE MOD(rn, 2) = 0
),
swapped_pairs AS (
  SELECT
    o.id AS id1,
    e.val AS val1,
    e.id AS id2,
    o.val AS val2
  FROM odd_rows o
  LEFT JOIN even_rows e ON o.rn + 1 = e.rn
),
flattened AS (
  SELECT id1 AS id, val1 AS val FROM swapped_pairs WHERE val1 IS NOT NULL
  UNION ALL
  -- Only include val2 if id2 is NOT null
  SELECT id2 AS id, val2 AS val FROM swapped_pairs WHERE id2 IS NOT NULL
  UNION ALL
  -- Include the unmatched last row (e.g., Eve) if val1 is null (i.e., no pair found)
  SELECT id1 AS id, val2 AS val FROM swapped_pairs WHERE val1 IS NULL
)

SELECT id, val
FROM flattened
ORDER BY id;
-- select * from swapped_pairs
