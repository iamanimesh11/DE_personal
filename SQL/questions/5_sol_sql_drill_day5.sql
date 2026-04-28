CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    country VARCHAR(50),
    created_at DATE
);

CREATE TABLE subscriptions (
    sub_id VARCHAR(10) PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    plan VARCHAR(20),
    started_at DATE,
    ended_at DATE,
    status VARCHAR(20),
    amount DECIMAL(10, 2)
);

CREATE TABLE payments (
    pay_id VARCHAR(10) PRIMARY KEY,
    sub_id VARCHAR(10) REFERENCES subscriptions(sub_id),
    paid_at DATE,
    amount DECIMAL(10, 2),
    status VARCHAR(20)
);

CREATE TABLE events (
    event_id VARCHAR(10) PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    event_type VARCHAR(50),
    occurred_at TIMESTAMP
);

INSERT INTO users VALUES
(1, 'Animesh', 'animesh@gmail.com', 'India', '2023-01-15'),
(2, 'Rohit', 'rohit@gmail.com', 'India', '2023-02-10'),
(3, 'Sara', 'sara@outlook.com', 'USA', '2023-03-05'),
(4, 'Karan', 'karan@gmail.com', 'India', '2023-04-20'),
(5, 'Nina', 'nina@yahoo.com', 'UK', '2023-05-01'),
(6, 'Dev', 'dev@gmail.com', 'India', '2023-06-15'),
(7, 'Animesh', 'animesh@gmail.com', 'India', '2023-01-20'),
(8, 'Rohit', 'rohit@gmail.com', 'India', '2023-02-10');


INSERT INTO subscriptions VALUES
('S01', 1, 'basic', '2023-01-15', '2023-04-15', 'expired', 299.00),
('S02', 1, 'pro', '2023-04-16', NULL, 'active', 799.00),
('S03', 2, 'pro', '2023-02-10', '2023-05-10', 'expired', 799.00),
('S04', 2, 'basic', '2023-05-11', NULL, 'active', 299.00),
('S05', 3, 'enterprise', '2023-03-05', NULL, 'active', 2999.00),
('S06', 4, 'basic', '2023-04-20', '2023-07-20', 'expired', 299.00),
('S07', 4, 'basic', '2023-07-21', '2023-10-21', 'expired', 299.00),
('S08', 5, 'pro', '2023-05-01', NULL, 'active', 799.00),
('S09', 6, 'basic', '2023-06-15', NULL, 'active', 299.00),
('S10', 3, 'enterprise', '2023-01-01', '2023-02-28', 'expired', 2999.00),
('S11', 1, 'pro', '2023-04-16', NULL, 'active', 799.00),
('S12', 3, 'enterprise', '2023-03-05', NULL, 'active', 2999.00),
('S13', 1, 'basic', '2023-04-10', '2023-04-20', 'expired', 299.00);


INSERT INTO payments VALUES
('P01', 'S01', '2023-01-15', 299.00, 'success'),
('P02', 'S02', '2023-04-16', 799.00, 'success'),
('P03', 'S03', '2023-02-10', 799.00, 'success'),
('P04', 'S04', '2023-05-11', 299.00, 'success'),
('P05', 'S05', '2023-03-05', 2999.00, 'success'),
('P06', 'S06', '2023-04-20', 299.00, 'success'),
('P07', 'S07', '2023-07-21', 299.00, 'success'),
('P08', 'S08', '2023-05-01', 799.00, 'success'),
('P09', 'S09', '2023-06-15', 299.00, 'success'),
('P10', 'S10', '2023-01-01', 2999.00, 'success'),
('P11', 'S02', '2023-05-16', 799.00, 'failed'),
('P12', 'S05', '2023-04-05', 2999.00, 'failed'),
('P13', 'S04', '2023-06-11', 299.00, 'success'),
('P14', 'S02', '2023-06-16', 799.00, 'success');

INSERT INTO events VALUES
('E01', 1, 'login', '2023-04-10 09:00:00'),
('E02', 1, 'feature_used', '2023-04-10 09:15:00'),
('E03', 2, 'login', '2023-05-12 10:00:00'),
('E04', 2, 'feature_used', '2023-05-12 10:30:00'),
('E05', 3, 'login', '2023-06-01 08:00:00'),
('E06', 4, 'login', '2023-08-01 11:00:00'),
('E07', 4, 'feature_used', '2023-08-01 11:05:00'),
('E08', 6, 'login', '2023-07-01 14:00:00'),
('E09', 1, 'login', '2023-06-16 10:00:00'),
('E10', 3, 'feature_used', '2023-06-01 08:45:00');




-- WITH plan_hierarchy AS (
--     SELECT 'enterprise' AS plan, 3 AS weight
--     UNION ALL SELECT 'pro', 2
--     UNION ALL SELECT 'basic', 1
-- ),

-- subscription_weights AS (
--     SELECT 
--         u.name,
--         s.plan,
--         s.started_at,
--         h.weight,
--         -- Get the plan name and weight of the previous subscription
--         LAG(s.plan) OVER (PARTITION BY s.user_id ORDER BY s.started_at) AS prev_plan,
--         LAG(h.weight) OVER (PARTITION BY s.user_id ORDER BY s.started_at) AS prev_weight
--     FROM subscriptions s
--     JOIN users u ON s.user_id = u.user_id
--     JOIN plan_hierarchy h ON s.plan = h.plan
-- )

-- SELECT 
--     name,
--     prev_plan AS "previous plan",
--     plan AS "new plan",
--     started_at AS "date of downgrade"
-- FROM subscription_weights
-- WHERE prev_weight > weight;




-- q2



-- SELECT 
--     s.plan,
--     SUM(p.amount) AS revenue
-- FROM subscriptions s
-- JOIN payments p ON s.sub_id = p.sub_id
-- WHERE p.status = 'success'
-- GROUP BY s.plan;



-- 3
-- select * from (
-- SELECT 
-- user_id,name,email,country,created_at ,
-- row_number() over (PARTITION by email order by created_at,user_id) as rn 
-- from users
-- ) a 
-- where rn=1


-- 4 

-- SELECT distinct p1.amount
-- FROM payments p1
-- WHERE 2 = (
--     SELECT COUNT( p2.amount)
--     FROM payments p2
--     WHERE p2.amount > p1.amount
--       AND p2.status = 'success'
-- )
-- AND p1.status = 'success';




-- 5 

-- select * from subscriptions;




-- with user_Activity as (

-- select u.user_id,
-- u.name,

-- max(case when s.status="active" then 1 else 0 end ) as has_Active,
-- max(case when s.status="expired" then 1 else 0 end ) as has_expired,
-- max(case when e.event_type="login" and e.occurred_at>-'2023-08-01' - interval 60 day then 1 else 0 end ) as active_60d,
-- count(s.sub_id) as sub_count
-- from users u 
-- left join subscriptions s on u.user_id=s.user_id
-- left join events e on u.user_id=e.user_id
-- group by u.user_id,u.name

-- )

-- SELECT 
--     name,
--     CASE 
--         WHEN has_expired = 1 AND has_active = 0 AND active_60d = 0 THEN 'churned'
--         WHEN has_active = 1 AND active_60d = 0 THEN 'at_risk'
--         WHEN has_active = 1 AND active_60d = 1 THEN 'engaged'
--         WHEN sub_count = 0 THEN 'never_converted'
--         ELSE 'other' 
--     END AS lifecycle_stage
-- FROM user_activity;


-- SELECT * from subscriptions;

-- select user_id,started_at as gap_Start,
-- prev as gap_end from (
-- select user_id,started_at,
-- lag(started_at) over (PARTITION by user_id order by started_at) as prev 
-- from subscriptions 
-- ) a 
-- where prev is not Null




-- 6 

-- SELECT 
--     user_id, 
--     prev_end AS gap_start, 
--     started_at AS gap_end
-- FROM (
--     SELECT 
--         user_id, 
--         started_at,
--         -- Get the END date of the previous subscription
--         LAG(ended_at) OVER (PARTITION BY user_id ORDER BY started_at) AS prev_end
--     FROM subscriptions
-- ) a
-- -- A gap exists if the previous sub ended BEFORE the current one started
-- WHERE prev_end IS NOT NULL 
--   AND prev_end < started_at;


-- WITH user_subs AS (
--     SELECT 
--         u.name,
--         u.country,
--         u.created_at,
--         s.amount,
--         -- Find the highest amount among all seniors (earlier created_at)
--         MAX(s.amount) OVER (
--             PARTITION BY u.country 
--             ORDER BY u.created_at 
--         ) AS max_senior_amount
--     FROM users u
--     JOIN subscriptions s ON u.user_id = s.user_id
--     WHERE s.status = 'active'
-- )

-- select * from user_subs


-- 9

-- WITH ranked_subs AS (
--     SELECT 
--         u.user_id,
--         u.name,
--         s.plan AS first_plan,
--         s.started_at AS first_started_at,
--         ROW_NUMBER() OVER (
--             PARTITION BY u.user_id 
--             ORDER BY s.started_at ASC, s.sub_id ASC
--         ) as rn
--     FROM users u
--     JOIN subscriptions s ON u.user_id = s.user_id
-- )
-- SELECT 
--     user_id, 
--     name, 
--     first_plan, 
--     first_started_at
-- FROM ranked_subs
-- WHERE rn = 1 
--   AND first_plan = 'basic';


-- 9 

-- WITH user_payments AS (
--     -- CTE 1: Calculate raw totals per user
--     SELECT 
--         s.user_id,
--         SUM(CASE WHEN p.status = 'success' THEN p.amount ELSE 0 END) AS success_amount,
--         SUM(CASE WHEN p.status = 'failed' THEN p.amount ELSE 0 END) AS failed_amount,
--         SUM(p.amount) AS total_attempted
--     FROM subscriptions s
--     JOIN payments p ON s.sub_id = p.sub_id
--     GROUP BY s.user_id
-- ),
-- user_status AS (
--     -- CTE 2: Determine if they have ANY currently active plan
--     SELECT 
--         user_id,
--         MAX(CASE WHEN status = 'active' THEN 'yes' ELSE 'no' END) AS still_active
--     FROM subscriptions
--     GROUP BY user_id
-- ),
-- final_metrics AS (
--     -- CTE 3: Combine and calculate rates
--     SELECT 
--         u.user_id,
--         u.name,
--         p.success_amount,
--         p.failed_amount,
--         ROUND((p.failed_amount / p.total_attempted) * 100, 2) AS failure_rate,
--         s.still_active
--     FROM users u
--     JOIN user_payments p ON u.user_id = p.user_id
--     JOIN user_status s ON u.user_id = s.user_id
--     WHERE p.failed_amount > 0
-- )
-- SELECT * FROM final_metrics;






-- q10

select *
from subscriptions s1 
join subscriptions s2
on s1.user_id=s2.user_id
where 
s1.started_at between s2.started_at and s2.ended_at






