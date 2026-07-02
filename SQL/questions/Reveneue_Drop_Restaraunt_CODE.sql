-- SQL DAILY DRILL 
-- Food Delivery Platform — QuickBite
-- One Story · 10 Connected Questions · Business Investigation
-- Solved by: Animesh
-- ========================================================
-- 
-- SCENARIO
-- --------
-- You are a Senior Data Analyst at QuickBite. The Head of Growth flagged
-- an 18% revenue drop last quarter. Investigate city by city, restaurant
-- by restaurant, and build the full picture. Each question feeds the next.
-- 
-- Tables: customers, restaurants, orders, delivery_agents, deliveries
-- 
-- ========================================================
-- 
-- 
-- Q1 — Revenue Baseline (Net Revenue per City per Month)
-- -------------------------------------------------------
-- 
-- Find net revenue (total_amount - discount_applied) per city per month
-- for delivered orders only. Cancelled orders = zero revenue.
-- This is the foundation every other question references.
-- 
-- 
-- QUERY:
-- ------
WITH monthly_city_revenue AS (
    SELECT
        r.city,
        DATE_FORMAT(o.order_date, '%Y-%m') AS month,
        SUM(o.total_amount - o.discount_applied) AS net_revenue
    FROM orders o
    JOIN restaurants r ON r.restaurant_id = o.restaurant_id
    WHERE o.status = 'delivered'
    GROUP BY r.city, DATE_FORMAT(o.order_date, '%Y-%m')
)
SELECT * FROM monthly_city_revenue
ORDER BY city, month;


-- CONCLUSION:
-- -----------
-- Delhi and Mumbai both show strong January revenue (1690 and 1150) that
-- drops significantly by March (940 and 610). Bangalore and Chennai have
-- no March data at all — they either had no orders or only cancelled ones.
-- 
-- Next: Quantify the exact drop % for Delhi and Mumbai → Q2.
-- 
-- 
-- ========================================================
-- 
-- 
-- Q2 — Which Cities Are Declining?
-- ---------------------------------
-- 
-- From Q1 output, find cities where March 2024 revenue is lower than
-- January 2024. Compute absolute drop and percentage drop.
-- 
-- 
-- QUERY:
-- ------
WITH monthly_city_revenue AS (
    SELECT
        r.city,
        DATE_FORMAT(o.order_date, '%Y-%m') AS month,
        SUM(o.total_amount - o.discount_applied) AS net_revenue
    FROM orders o
    JOIN restaurants r ON r.restaurant_id = o.restaurant_id
    WHERE o.status = 'delivered'
    GROUP BY r.city, DATE_FORMAT(o.order_date, '%Y-%m')
),
revenue_summary AS (
    SELECT
        jan.city,
        jan.net_revenue AS jan_revenue,
        mar.net_revenue AS mar_revenue,
        (jan.net_revenue - mar.net_revenue) AS absolute_drop,
        ROUND(((jan.net_revenue - mar.net_revenue) / jan.net_revenue) * 100, 2) AS pct_drop
    FROM monthly_city_revenue jan
    JOIN monthly_city_revenue mar
        ON jan.city = mar.city
        AND jan.month = '2024-01'
        AND mar.month = '2024-03'
    WHERE mar.net_revenue < jan.net_revenue
)
SELECT * FROM revenue_summary;


-- CONCLUSION:
-- -----------
-- Delhi dropped 44.38% and Mumbai dropped 46.96% from Jan to March.
-- Both cities declined at nearly the same rate which rules out a
-- city-specific event — something platform-wide is causing this.
-- 
-- Next: Is this drop because fewer orders were placed, or because each
-- order was worth less? → Q3.
-- 
-- 
-- ========================================================
-- 
-- 
-- Q3 — Volume vs Value Breakdown
-- --------------------------------
-- 
-- For Delhi and Mumbai only: total orders placed, delivered orders,
-- and average net order value per month. This tells us whether customers
-- ordered less (volume drop) or spent less per order (value drop).
-- 
-- 
-- QUERY:
-- ------
WITH declining_cities AS ('Delhi', 'Mumbai')
SELECT
    r.city,
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    COUNT(o.order_id) AS total_orders,
    SUM(CASE WHEN o.status = 'delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    AVG(CASE WHEN o.status = 'delivered'
        THEN o.total_amount - o.discount_applied END) AS avg_net_order_value
FROM orders o
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE r.city IN ('Delhi', 'Mumbai')
GROUP BY r.city, DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY r.city, month;


-- CONCLUSION:
-- -----------
-- Delhi: Jan had 4 delivered orders, Feb had 2, March had only 1.
-- Avg order value actually went UP (622 → 790 → 940).
-- This is a volume collapse — customers who stayed are spending MORE,
-- but far fewer customers are ordering at all.
-- 
-- Mumbai tells the same story: Jan had 1 delivered order worth 1150,
-- March had 1 worth 610 — fewer customers, but the per-order spend trend
-- is mixed.
-- 
-- The problem is retention and acquisition, NOT product pricing.
-- 
-- Next: Which specific restaurants lost orders in these cities? → Q4.
-- 
-- 
-- ========================================================
-- 
-- 
-- Q4 — Restaurant Drop-Off Analysis
-- -----------------------------------
-- 
-- For each restaurant in Delhi and Mumbai, compare Jan vs Mar order count.
-- Flag as: dropped_off (had Jan orders, zero in Mar),
-- retained (had orders in both), never_active (zero in both).
-- 
-- 
-- QUERY:
-- ------
SELECT
    r.restaurant_id,
    r.name,
    r.city,
    SUM(CASE WHEN o.order_date >= '2024-01-01'
             AND o.order_date < '2024-02-01' THEN 1 ELSE 0 END) AS jan_orders,
    SUM(CASE WHEN o.order_date >= '2024-03-01'
             AND o.order_date < '2024-04-01' THEN 1 ELSE 0 END) AS mar_orders,
    CASE
        WHEN SUM(CASE WHEN o.order_date >= '2024-01-01'
                      AND o.order_date < '2024-02-01' THEN 1 ELSE 0 END) > 0
         AND SUM(CASE WHEN o.order_date >= '2024-03-01'
                      AND o.order_date < '2024-04-01' THEN 1 ELSE 0 END) = 0
            THEN 'dropped_off'
        WHEN SUM(CASE WHEN o.order_date >= '2024-01-01'
                      AND o.order_date < '2024-02-01' THEN 1 ELSE 0 END) > 0
         AND SUM(CASE WHEN o.order_date >= '2024-03-01'
                      AND o.order_date < '2024-04-01' THEN 1 ELSE 0 END) > 0
            THEN 'retained'
        ELSE 'never_active'
    END AS status
FROM restaurants r
JOIN orders o ON r.restaurant_id = o.restaurant_id
WHERE r.city IN ('Delhi', 'Mumbai')
GROUP BY r.restaurant_id, r.name, r.city
ORDER BY r.city, r.restaurant_id;


-- CONCLUSION:
-- -----------
-- Dropped off in Delhi: Burger King (R01) and Kebab Corner (R07).
-- Dropped off in Mumbai: The Burger Lab (R06).
-- Retained: Spice Garden (R03) in Delhi and Pizza Hut (R02) in Mumbai.
-- 
-- Three restaurants completely lost all demand in March. This could be
-- slow delivery, bad experience, or competitor undercutting on price.
-- 
-- Next: Was delivery time the issue for dropped restaurants? → Q5.
-- 
-- 
-- ========================================================
-- 
-- 
-- Q5 — Delivery Time vs Platform Average
-- ----------------------------------------
-- 
-- For dropped_off restaurants only, compute their actual avg delivery
-- time using TIMESTAMPDIFF on deliveries table timestamps — NOT the
-- pre-computed column in orders. Compare to platform average.
-- Flag restaurants above platform avg.
-- 
-- 
-- QUERY:
-- ------
WITH platform_avg AS (
    SELECT
        ROUND(AVG(TIMESTAMPDIFF(MINUTE, d.pickup_time, d.drop_time)), 2)
            AS platform_avg_min
    FROM deliveries d
    WHERE d.drop_time > d.pickup_time
)
SELECT
    r.restaurant_id,
    r.name,
    ROUND(AVG(TIMESTAMPDIFF(MINUTE, d.pickup_time, d.drop_time)), 2)
        AS avg_delivery_min,
    p.platform_avg_min,
    CASE
        WHEN AVG(TIMESTAMPDIFF(MINUTE, d.pickup_time, d.drop_time))
             > p.platform_avg_min THEN 'yes'
        ELSE 'no'
    END AS above_platform_avg
FROM orders o
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
JOIN deliveries d ON d.order_id = o.order_id
CROSS JOIN platform_avg p
WHERE r.restaurant_id IN ('R01', 'R07', 'R06')
  AND d.drop_time > d.pickup_time
GROUP BY r.restaurant_id, r.name, p.platform_avg_min;


-- CONCLUSION:
-- -----------
-- Burger King (R01): 36.5 min — FASTER than platform avg (47 min).
-- The Burger Lab (R06): 40 min — FASTER than platform avg.
-- Kebab Corner (R07): 52 min — SLOWER than platform avg.
-- 
-- Delivery time is NOT the reason R01 and R06 lost customers.
-- Something else caused their drop — likely competitor promotions,
-- visibility on the app, or pricing. Kebab Corner is the only one
-- with a legitimate delivery experience problem.
-- 
-- Next: Are the customers we are losing high-value ones? → Q6.
-- 
-- 
-- ========================================================
-- 
-- 
-- Q6 — Are We Losing High-Value Customers?
-- ------------------------------------------
-- 
-- Find Delhi and Mumbai customers who placed at least one order in
-- January but ZERO orders in Feb + March combined.
-- Classify as high_value (lifetime net revenue > 1000) or low_value.
-- 
-- 
-- QUERY:
-- ------
WITH customer_activity AS (
    SELECT
        c.customer_id,
        c.name,
        c.city,
        SUM(CASE WHEN o.order_date >= '2024-01-01'
                 AND o.order_date < '2024-02-01' THEN 1 ELSE 0 END) AS jan_orders,
        SUM(CASE WHEN o.order_date >= '2024-02-01'
                 AND o.order_date < '2024-04-01' THEN 1 ELSE 0 END) AS feb_mar_orders,
        SUM(o.total_amount - o.discount_applied) AS lifetime_net_revenue
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.city IN ('Delhi', 'Mumbai')
    GROUP BY c.customer_id, c.name, c.city
)
SELECT
    customer_id,
    name,
    city,
    ROUND(lifetime_net_revenue, 2) AS lifetime_net_revenue,
    CASE
        WHEN lifetime_net_revenue > 1000 THEN 'high_value'
        ELSE 'low_value'
    END AS segment
FROM customer_activity
WHERE jan_orders >= 1
  AND feb_mar_orders = 0
ORDER BY lifetime_net_revenue DESC;


-- CONCLUSION:
-- -----------
-- C09 (Siddharth, Delhi) placed one order in Jan worth 1200 net revenue
-- and then disappeared entirely. He is classified as high_value.
-- This is a critical signal — a high-spending new customer was acquired
-- but not retained past month 1.
-- 
-- None of the original customers from earlier cohorts fully churned in
-- this window — the loss is concentrated in new signups.
-- 
-- Next: Which agents are slowest in declining cities? → Q7.
-- 
-- 
-- ========================================================
-- 
-- 
-- Q7 — Delivery Agent Performance by City
-- -----------------------------------------
-- 
-- For each agent: total deliveries, avg speed (distance_km divided by
-- actual minutes from timestamps), and rank within city by speed.
-- Rank 1 = fastest. Identify slowest agents in Delhi and Mumbai.
-- 
-- 
-- QUERY:
-- ------
WITH agent_stats AS (
    SELECT
        da.agent_id,
        da.name,
        da.city,
        COUNT(d.delivery_id) AS total_deliveries,
        AVG(d.distance_km / NULLIF(
            TIMESTAMPDIFF(MINUTE, d.pickup_time, d.drop_time), 0)
        ) AS avg_speed_km_per_min
    FROM deliveries d
    JOIN delivery_agents da ON d.agent_id = da.agent_id
    WHERE d.drop_time > d.pickup_time
    GROUP BY da.agent_id, da.name, da.city
)
SELECT
    *,
    DENSE_RANK() OVER (
        PARTITION BY city
        ORDER BY avg_speed_km_per_min DESC
    ) AS city_speed_rank
FROM agent_stats
ORDER BY city, city_speed_rank;


-- CONCLUSION:
-- -----------
-- In Delhi: Ramesh (A03) is faster than Vijay (A01). Vijay is the slowest
-- in Delhi. High-value orders in Delhi should be routed to Ramesh first.
-- 
-- In Mumbai: Suresh (A02) handles all Mumbai deliveries and has reasonable
-- speed — no immediate concern here.
-- 
-- Slowest agent per city: Vijay (Delhi), Suresh (Mumbai — only agent there).
-- 
-- Next: Which customers are cancelling most, and are they concentrated
-- in declining cities? → Q8.
-- 
-- 
-- ========================================================
-- 
-- 
-- Q8 — Cancellation Profile
-- ---------------------------
-- 
-- For every customer with at least one cancelled order: total orders,
-- cancelled count, cancellation rate, and whether their rate is above
-- platform average. Platform avg = total cancelled / total orders.
-- 
-- 
-- QUERY:
-- ------
WITH platform_baseline AS (
    SELECT
        AVG(CASE WHEN status = 'cancelled' THEN 1.0 ELSE 0.0 END)
            AS global_avg_rate
    FROM orders
),
customer_cancel AS (
    SELECT
        c.customer_id,
        c.name,
        c.city,
        COUNT(o.order_id) AS total_orders,
        SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
        ROUND(
            SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END)
            / COUNT(o.order_id), 2
        ) AS cancel_rate
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name, c.city
    HAVING SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) >= 1
)
SELECT
    cc.*,
    CASE
        WHEN cc.cancel_rate > pb.global_avg_rate THEN 'yes'
        ELSE 'no'
    END AS above_platform_avg
FROM customer_cancel cc
CROSS JOIN platform_baseline pb
ORDER BY cc.cancel_rate DESC;


-- CONCLUSION:
-- -----------
-- Platform avg cancellation rate = 3 cancelled / 21 total = 0.143.
-- 
-- Dev (C06, Delhi): 50% cancel rate — highest on platform.
-- Rohit (C02, Mumbai): 33% cancel rate.
-- Priya (C07, Bangalore): 33% cancel rate.
-- 
-- All three high-cancel customers are in the exact cities showing
-- revenue decline (Delhi and Mumbai). This is not a coincidence —
-- cancellations remove revenue AND distort demand signals for restaurants,
-- which may cause restaurants to deprioritize the platform.
-- 
-- Next: Are newer customer cohorts spending less than older ones? → Q9.
-- 
-- 
-- ========================================================
-- 
-- 
-- Q9 — Cohort Revenue Retention
-- -------------------------------
-- 
-- Group customers by signup month. For each cohort, compute total net
-- revenue per calendar month in 2024, cohort size, and revenue
-- per customer. This reveals if newer cohorts monetize worse.
-- 
-- 
-- QUERY:
-- ------
WITH cohort_sizes AS (
    SELECT
        DATE_FORMAT(signup_date, '%Y-%m') AS cohort,
        COUNT(customer_id) AS cohort_size
    FROM customers
    GROUP BY DATE_FORMAT(signup_date, '%Y-%m')
),
monthly_revenue AS (
    SELECT
        DATE_FORMAT(c.signup_date, '%Y-%m') AS cohort,
        DATE_FORMAT(o.order_date, '%Y-%m') AS month,
        SUM(o.total_amount - o.discount_applied) AS net_revenue
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_date >= '2024-01-01'
      AND o.order_date < '2024-04-01'
      AND o.status = 'delivered'
    GROUP BY
        DATE_FORMAT(c.signup_date, '%Y-%m'),
        DATE_FORMAT(o.order_date, '%Y-%m')
)
SELECT
    mr.cohort,
    mr.month,
    cs.cohort_size,
    ROUND(mr.net_revenue, 2) AS net_revenue,
    ROUND(mr.net_revenue / cs.cohort_size, 2) AS revenue_per_customer
FROM monthly_revenue mr
JOIN cohort_sizes cs ON mr.cohort = cs.cohort
ORDER BY mr.cohort, mr.month;


-- CONCLUSION:
-- -----------
-- Jan 2023 cohort (Animesh): generated 1690 in Jan 2024 — highest
-- revenue per customer of any cohort. This is a loyal, high-spending user.
-- 
-- Jan 2024 cohort (Siddharth): generated 1200 in Jan but nothing after.
-- New customers are being acquired but drop off immediately after first order.
-- 
-- Mar 2023 cohort shows multi-month activity in Feb and Mar 2024 which
-- confirms that older cohorts have stronger retention — the onboarding
-- or early engagement experience for new signups is broken.
-- 
-- Next: Synthesize all of this into one final verdict → Q10.
-- 
-- 
-- ========================================================
-- 
-- 
-- Q10 — Final Verdict: Unified Drop Explanation
-- -----------------------------------------------
-- 
-- Single query with 4+ chained CTEs. For each declining city (Delhi,
-- Mumbai): jan revenue, mar revenue, drop %, dominant drop reason
-- (volume_drop / value_drop / both / other), top dropped restaurant,
-- slowest agent, and count of high-cancel customers.
-- 
-- 
-- QUERY:
-- ------
WITH platform_cancel_baseline AS (
    SELECT
        AVG(CASE WHEN status = 'cancelled' THEN 1.0 ELSE 0.0 END)
            AS global_avg_rate
    FROM orders
),
city_revenue_metrics AS (
    SELECT
        r.city,
        SUM(CASE WHEN o.order_date >= '2024-01-01'
                 AND o.order_date < '2024-02-01'
                 THEN o.total_amount - o.discount_applied ELSE 0 END) AS jan_rev,
        SUM(CASE WHEN o.order_date >= '2024-03-01'
                 AND o.order_date < '2024-04-01'
                 THEN o.total_amount - o.discount_applied ELSE 0 END) AS mar_rev,
        COUNT(CASE WHEN o.order_date >= '2024-01-01'
                   AND o.order_date < '2024-02-01'
                   AND o.status = 'delivered' THEN o.order_id END) AS jan_vol,
        COUNT(CASE WHEN o.order_date >= '2024-03-01'
                   AND o.order_date < '2024-04-01'
                   AND o.status = 'delivered' THEN o.order_id END) AS mar_vol,
        AVG(CASE WHEN o.order_date >= '2024-01-01'
                 AND o.order_date < '2024-02-01'
                 AND o.status = 'delivered'
                 THEN o.total_amount - o.discount_applied END) AS jan_aov,
        AVG(CASE WHEN o.order_date >= '2024-03-01'
                 AND o.order_date < '2024-04-01'
                 AND o.status = 'delivered'
                 THEN o.total_amount - o.discount_applied END) AS mar_aov
    FROM restaurants r
    JOIN orders o ON r.restaurant_id = o.restaurant_id
    WHERE r.city IN ('Delhi', 'Mumbai')
    GROUP BY r.city
),
restaurant_ranks AS (
    SELECT
        r.city,
        r.name AS restaurant_name,
        ROW_NUMBER() OVER (
            PARTITION BY r.city
            ORDER BY COUNT(CASE WHEN o.order_date >= '2024-01-01'
                                AND o.order_date < '2024-02-01'
                                THEN o.order_id END) DESC,
                     r.restaurant_id ASC
        ) AS r_rank
    FROM restaurants r
    JOIN orders o ON r.restaurant_id = o.restaurant_id
    WHERE r.city IN ('Delhi', 'Mumbai')
    GROUP BY r.city, r.restaurant_id, r.name
    HAVING COUNT(CASE WHEN o.order_date >= '2024-01-01'
                      AND o.order_date < '2024-02-01'
                      THEN o.order_id END) > 0
       AND COUNT(CASE WHEN o.order_date >= '2024-03-01'
                      AND o.order_date < '2024-04-01'
                      THEN o.order_id END) = 0
),
top_dropped AS (
    SELECT city, restaurant_name
    FROM restaurant_ranks
    WHERE r_rank = 1
),
agent_speeds AS (
    SELECT
        da.city,
        da.name AS agent_name,
        ROW_NUMBER() OVER (
            PARTITION BY da.city
            ORDER BY AVG(
                d.distance_km / NULLIF(
                    TIMESTAMPDIFF(MINUTE, d.pickup_time, d.drop_time), 0)
            ) ASC,
            da.agent_id ASC
        ) AS speed_rank
    FROM deliveries d
    JOIN delivery_agents da ON d.agent_id = da.agent_id
    WHERE d.drop_time > d.pickup_time
    GROUP BY da.city, da.agent_id, da.name
),
slowest_agents AS (
    SELECT city, agent_name
    FROM agent_speeds
    WHERE speed_rank = 1
),
high_cancel_customers AS (
    SELECT
        c.city,
        COUNT(DISTINCT c.customer_id) AS high_cancel_count
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    CROSS JOIN platform_cancel_baseline pcb
    WHERE c.city IN ('Delhi', 'Mumbai')
    GROUP BY c.city, pcb.global_avg_rate
    HAVING AVG(CASE WHEN o.status = 'cancelled'
                    THEN 1.0 ELSE 0.0 END) > pcb.global_avg_rate
)
SELECT
    crm.city,
    ROUND(crm.jan_rev, 2) AS jan_net_revenue,
    ROUND(crm.mar_rev, 2) AS mar_net_revenue,
    ROUND(((crm.jan_rev - crm.mar_rev) / NULLIF(crm.jan_rev, 0)) * 100, 2)
        AS revenue_drop_pct,
    CASE
        WHEN ((crm.jan_vol - crm.mar_vol) / NULLIF(crm.jan_vol, 0)) > 0.30
         AND ((crm.jan_aov - crm.mar_aov) / NULLIF(crm.jan_aov, 0)) > 0.30
            THEN 'both'
        WHEN ((crm.jan_vol - crm.mar_vol) / NULLIF(crm.jan_vol, 0)) > 0.30
            THEN 'volume_drop'
        WHEN ((crm.jan_aov - crm.mar_aov) / NULLIF(crm.jan_aov, 0)) > 0.30
            THEN 'value_drop'
        ELSE 'other'
    END AS dominant_drop_reason,
    COALESCE(td.restaurant_name, 'None') AS top_dropped_restaurant,
    COALESCE(sa.agent_name, 'None')      AS slowest_agent,
    COALESCE(hcc.high_cancel_count, 0)  AS high_cancel_customers
FROM city_revenue_metrics crm
LEFT JOIN top_dropped td         ON crm.city = td.city
LEFT JOIN slowest_agents sa      ON crm.city = sa.city
LEFT JOIN high_cancel_customers hcc ON crm.city = hcc.city;


-- CONCLUSION:
-- -----------
-- Delhi:  -44.38% revenue. Dominant reason = volume_drop.
--         Top dropped restaurant = Burger King.
--         Slowest agent = Vijay.
--         High-cancel customers = 1 (Dev, 50% rate).
-- 
-- Mumbai: -46.96% revenue. Dominant reason = volume_drop.
--         Top dropped restaurant = The Burger Lab.
--         Slowest agent = Suresh (only agent in Mumbai).
--         High-cancel customers = 1 (Rohit, 33% rate).
-- 
-- WHAT THIS MEANS FOR THE BUSINESS:
-- - Both cities collapsed for the same reason: far fewer orders placed,
--   not lower spend per order. Customers who stayed actually spent more.
-- - The problem is at the top of the funnel — acquisition and early
--   retention of new customers is broken.
-- - Burger King and The Burger Lab losing all demand despite fast delivery
--   suggests a visibility or promotional issue, not a quality issue.
-- - Kebab Corner is the only dropped restaurant with a real delivery
--   problem (52 min vs 47 min platform avg) — worth an SLA review.
-- - High-cancel customers (Dev, Rohit) are exactly in the declining cities.
--   Cancellations damage restaurant revenue signals and platform reputation.
-- 
-- RECOMMENDED ACTIONS:
-- 1. Re-engagement campaign for Jan 2024 new signups before they churn.
-- 2. Investigate why Burger King and The Burger Lab had zero March orders
--    — check competitor promotions and app ranking changes in that period.
-- 3. Assign high-value Delhi orders to Ramesh (faster) over Vijay.
-- 4. Review Kebab Corner delivery SLA — consider penalty or coaching.
-- 5. Monitor Dev and Rohit for repeat cancellations — offer or account flag.
-- 
-- 
-- ========================================================
-- END OF DAY 8
-- ========================================================