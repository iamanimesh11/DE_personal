-- 1. Create Customers Table
CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50),
    city VARCHAR(50),
    signup_date DATE,
    plan VARCHAR(20)
);

-- 2. Create Restaurants Table
CREATE TABLE restaurants (
    restaurant_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(50),
    cuisine VARCHAR(50),
    avg_prep_time_min INT,
    rating DECIMAL(2, 1)
);

-- 3. Create Orders Table
CREATE TABLE orders (
    order_id VARCHAR(10) PRIMARY KEY,
    customer_id VARCHAR(10),
    restaurant_id VARCHAR(10),
    order_date DATE,
    delivery_time_min INT,
    status VARCHAR(20),
    total_amount DECIMAL(10, 2),
    discount_applied DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

-- 4. Create Delivery Agents Table
CREATE TABLE delivery_agents (
    agent_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50),
    city VARCHAR(50),
    joined_date DATE,
    vehicle VARCHAR(20)
);

-- 5. Create Deliveries Table
CREATE TABLE deliveries (
    delivery_id VARCHAR(10) PRIMARY KEY,
    order_id VARCHAR(10),
    agent_id VARCHAR(10),
    pickup_time DATETIME,
    drop_time DATETIME,
    distance_km DECIMAL(4, 1),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (agent_id) REFERENCES delivery_agents(agent_id)

);


-- Insert into Customers
INSERT INTO customers (customer_id, name, city, signup_date, plan) VALUES
('C01', 'Animesh', 'Delhi', '2023-01-10', 'gold'),
('C02', 'Rohit', 'Mumbai', '2023-02-15', 'silver'),
('C03', 'Sara', 'Delhi', '2023-03-01', 'gold'),
('C04', 'Karan', 'Bangalore', '2023-03-20', 'bronze'),
('C05', 'Nina', 'Mumbai', '2023-04-05', 'silver'),
('C06', 'Dev', 'Delhi', '2023-05-10', 'bronze'),
('C07', 'Priya', 'Bangalore', '2023-06-01', 'gold'),
('C08', 'Meera', 'Chennai', '2023-06-15', 'silver'),
('C09', 'Siddharth', 'Delhi', '2024-01-02', 'gold');

-- Insert into Restaurants
INSERT INTO restaurants (restaurant_id, name, city, cuisine, avg_prep_time_min, rating) VALUES
('R01', 'Burger King', 'Delhi', 'FastFood', 15, 4.2),
('R02', 'Pizza Hut', 'Mumbai', 'Italian', 20, 4.5),
('R03', 'Spice Garden', 'Delhi', 'Indian', 25, 4.8),
('R04', 'Wok Express', 'Bangalore', 'Chinese', 18, 4.1),
('R05', 'South Spice', 'Chennai', 'Indian', 30, 4.6),
('R06', 'The Burger Lab', 'Mumbai', 'FastFood', 12, 4.3),
('R07', 'Kebab Corner', 'Delhi', 'Indian', 22, 4.0),
('R08', 'Dragon Palace', 'Bangalore', 'Chinese', 20, 4.4);

-- Insert into Orders
INSERT INTO orders (order_id, customer_id, restaurant_id, order_date, delivery_time_min, status, total_amount, discount_applied) VALUES
('O001', 'C01', 'R01', '2024-01-05', 35, 'delivered', 450.00, 50.00),
('O002', 'C01', 'R03', '2024-01-12', 55, 'delivered', 820.00, 0.00),
('O003', 'C02', 'R02', '2024-01-08', 40, 'delivered', 650.00, 100.00),
('O004', 'C02', 'R06', '2024-01-20', 30, 'cancelled', 380.00, 0.00),
('O005', 'C03', 'R01', '2024-01-15', 38, 'delivered', 520.00, 50.00),
('O006', 'C03', 'R03', '2024-02-02', 60, 'delivered', 910.00, 0.00),
('O007', 'C04', 'R04', '2024-01-18', 42, 'delivered', 340.00, 0.00),
('O008', 'C04', 'R08', '2024-02-10', 50, 'delivered', 490.00, 50.00),
('O009', 'C05', 'R02', '2024-01-22', 45, 'delivered', 720.00, 100.00),
('O010', 'C05', 'R06', '2024-02-05', 28, 'delivered', 410.00, 0.00),
('O011', 'C06', 'R07', '2024-01-25', 52, 'delivered', 380.00, 0.00),
('O012', 'C06', 'R01', '2024-02-14', 48, 'cancelled', 420.00, 50.00),
('O013', 'C07', 'R04', '2024-02-08', 35, 'delivered', 560.00, 0.00),
('O014', 'C07', 'R08', '2024-02-20', 40, 'delivered', 630.00, 50.00),
('O015', 'C08', 'R05', '2024-01-30', 65, 'delivered', 780.00, 0.00),
('O016', 'C08', 'R05', '2024-02-18', 70, 'delivered', 850.00, 0.00),
('O017', 'C01', 'R07', '2024-02-25', 58, 'delivered', 670.00, 0.00),
('O018', 'C03', 'R03', '2024-03-05', 62, 'delivered', 940.00, 0.00),
('O019', 'C02', 'R02', '2024-03-10', 44, 'delivered', 710.00, 100.00),
('O020', 'C07', 'R04', '2024-03-15', 38, 'cancelled', 490.00, 0.00),
('O021', 'C09', 'R01', '2024-01-10', 32, 'delivered', 1300.00, 100.00);
-- Insert into Delivery Agents
INSERT INTO delivery_agents (agent_id, name, city, joined_date, vehicle) VALUES
('A01', 'Vijay', 'Delhi', '2022-06-01', 'bike'),
('A02', 'Suresh', 'Mumbai', '2022-08-15', 'bike'),
('A03', 'Ramesh', 'Delhi', '2023-01-10', 'scooter'),
('A04', 'Dinesh', 'Bangalore', '2022-11-20', 'bike'),
('A05', 'Mahesh', 'Chennai', '2023-03-05', 'scooter');

-- Insert into Deliveries
INSERT INTO deliveries (delivery_id, order_id, agent_id, pickup_time, drop_time, distance_km) VALUES
('D01', 'O001', 'A01', '2024-01-05 12:20:00', '2024-01-05 12:55:00', 4.2),
('D02', 'O002', 'A03', '2024-01-12 19:30:00', '2024-01-12 20:25:00', 6.8),
('D03', 'O003', 'A02', '2024-01-08 13:10:00', '2024-01-08 13:50:00', 5.1),
('D04', 'O005', 'A01', '2024-01-15 20:05:00', '2024-01-15 20:43:00', 3.9),
('D05', 'O006', 'A03', '2024-02-02 20:15:00', '2024-02-02 21:15:00', 7.2),
('D06', 'O007', 'A04', '2024-01-18 14:00:00', '2024-01-18 14:42:00', 4.5),
('D07', 'O008', 'A04', '2024-02-10 19:30:00', '2024-02-10 20:20:00', 5.8),
('D08', 'O009', 'A02', '2024-01-22 20:10:00', '2024-01-22 20:55:00', 6.0),
('D09', 'O010', 'A02', '2024-02-05 13:00:00', '2024-02-05 13:28:00', 3.2),
('D10', 'O011', 'A03', '2024-01-25 21:00:00', '2024-01-25 21:52:00', 5.5),
('D11', 'O013', 'A04', '2024-02-08 19:15:00', '2024-02-08 19:50:00', 4.1),
('D12', 'O014', 'A04', '2024-02-20 20:00:00', '2024-02-20 20:40:00', 4.8),
('D13', 'O015', 'A05', '2024-01-30 20:30:00', '2024-01-30 21:35:00', 8.5),
('D14', 'O016', 'A05', '2024-02-18 19:45:00', '2024-02-18 20:55:00', 9.0),
('D15', 'O017', 'A01', '2024-02-25 21:10:00', '2024-02-25 22:08:00', 6.5),
('D16', 'O018', 'A03', '2024-03-05 20:00:00', '2024-03-05 21:02:00', 7.0),
('D17', 'O019', 'A02', '2024-03-10 13:20:00', '2024-03-10 14:04:00', 5.3),
('D18', 'O021', 'A01', '2024-01-10 13:00:00', '2024-01-10 13:32:00', 3.5);



-- Q1 


with monthly_city_revenue  as  (
select r.city,DATE_FORMAT(order_date, '%Y-%m') as month ,
sum(o.total_amount - o.discount_applied) as net_Revenue
from orders o 
join restaurants r 
on r.restaurant_id = o.restaurant_id and  o.status="delivered"
group by r.city,DATE_FORMAT(order_date, '%Y-%m')
),
revenue_summary  as 
(select c1.city,c2.month as jan_month ,c1.month  as march_month,
c2.net_Revenue AS JAN_REVENUE ,c1.net_Revenue AS MAR_REVENUE,
(c2.net_revenue - c1.net_revenue) AS absolute_drop,
    ROUND(((c2.net_revenue - c1.net_revenue) / c2.net_revenue) * 100, 2) AS pct_drop
     from monthly_city_revenue  c1 
 JOIN monthly_city_revenue  c2 ON c1.city = c2.city  -- Added crucial join predicate
where c1.month="2024-03" and c2.month ="2024-01"
and c1.net_Revenue<c2.net_Revenue
)
, monthly_order_metrics  as (
select  r.city,DATE_FORMAT(o.order_date, '%Y-%m')  as month  ,
count(o.order_id) as total_orders,
sum(case when o.status="delivered" then 1 else 0 end) as delivered_orders,
sum(o.total_amount -o.discount_applied)/sum(case when o.status="delivered" then 1 else 0 end) as avg_net_order_value
from revenue_summary r 
join restaurants re 
on r.city = re.city 
join orders o 
on re.restaurant_id=o.restaurant_id
group by 
r.city ,
DATE_FORMAT(o.order_date, '%Y-%m')
order by r.city
),
restaurant_orders as (
SELECT 
    r.restaurant_id, 
    r.name,
    r.city, 
    SUM(CASE WHEN o.order_date >= '2024-01-01' AND o.order_date < '2024-02-01' THEN 1 ELSE 0 END) AS jan_orders, 
    SUM(CASE WHEN o.order_date >= '2024-03-01' AND o.order_date < '2024-04-01' THEN 1 ELSE 0 END) AS mar_orders 
FROM restaurants r 
JOIN orders o ON r.restaurant_id = o.restaurant_id 
WHERE r.city IN (SELECT DISTINCT city FROM monthly_order_metrics)
GROUP BY r.restaurant_id, r.name, r.city
),
restaurant_orders_declining as (
SELECT 
    r.restaurant_id,
    r.name,
    r.city,
    r.jan_orders,
    r.mar_orders,
    CASE 
        WHEN r.jan_orders > 0 AND r.mar_orders = 0 THEN 'dropped_off'
        WHEN r.jan_orders > 0 AND r.mar_orders > 0 THEN 'retained'
        WHEN r.jan_orders = 0 AND r.mar_orders = 0 THEN 'never_active'
        ELSE 'new_or_other' -- Handles cases where Jan = 0 but March > 0
    END AS status
FROM restaurant_orders r 
ORDER BY city DESC, restaurant_id ASC
),platform_stats AS (
    -- Step 1: Calculate the overall baseline average across ALL delivered orders
    SELECT ROUND(AVG(delivery_time_min), 2) AS platform_avg_delivery_min
    FROM orders
    WHERE delivery_time_min IS NOT NULL
)

-- q5 
,dropped_off_delivery_analysis as (
SELECT 
    r.restaurant_id,
    r.name,
    ROUND(AVG(o.delivery_time_min), 2) AS avg_delivery_time_min,
    p.platform_avg_delivery_min,
    CASE 
        WHEN AVG(o.delivery_time_min) > p.platform_avg_delivery_min THEN 'yes'
        ELSE 'no'
    END AS above_platform_avg
FROM orders o 
JOIN restaurants r ON r.restaurant_id = o.restaurant_id 
CROSS JOIN platform_stats p -- Injects the global average into every row safely6
WHERE r.restaurant_id IN (
    SELECT restaurant_id 
    FROM restaurant_orders_declining 
    WHERE status = 'dropped_off'
)
GROUP BY r.restaurant_id, r.name, p.platform_avg_delivery_min
ORDER BY r.restaurant_id ASC
)
-- RO1 & RO6 both restaurants were delivering food significantly faster than the platform baseline


-- q6 
, customer_order_periods AS (
    -- Step 1: Calculate order counts for January vs (February + March) for Delhi & Mumbai customers
    SELECT 
        c.customer_id,
        c.name,
        c.city,
        SUM(CASE WHEN o.order_date >= '2024-01-01' AND o.order_date < '2024-02-01' THEN 1 ELSE 0 END) AS jan_orders,
        SUM(CASE WHEN o.order_date >= '2024-02-01' AND o.order_date < '2024-04-01' THEN 1 ELSE 0 END) AS feb_mar_orders,
        -- Total lifetime net revenue = total_amount minus any discounts
        SUM(o.total_amount - o.discount_applied) AS total_lifetime_net_revenue
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.city IN ('Delhi', 'Mumbai')
    GROUP BY c.customer_id, c.name, c.city
)
-- Step 2: Filter for churned cohorts and segment them by value
,cte as (SELECT 
    customer_id,
    name,
    city,
    ROUND(total_lifetime_net_revenue, 2) AS total_lifetime_net_revenue,
    CASE 
        WHEN total_lifetime_net_revenue > 1000 THEN 'high_value'
        ELSE 'low_value'
    END AS customer_segment
FROM customer_order_periods
WHERE jan_orders >= 1 
  AND feb_mar_orders = 0
ORDER BY total_lifetime_net_revenue DESC
)
-- Customer C09 has an order entry for January (2024-01-10), but no records are created for him in February or March.

-- Q7 — Which Delivery Agents Are Handling the Slowest Deliveries?
, delivery_Agent_Stat as (
SELECT 
    d.agent_id,
    da.name,
    da.city,
    COUNT(d.delivery_id) AS total_deliveries,
    -- Step 1: Calculate distance divided by safe minutes duration
    AVG(d.distance_km / TIMESTAMPDIFF(MINUTE, d.pickup_time, d.drop_time)) AS avg_speed_km_per_min
FROM deliveries d 
JOIN delivery_agents da ON d.agent_id = da.agent_id
-- Step 2: Ensure timestamps are valid and drop time is strictly after pickup time
WHERE d.drop_time > d.pickup_time 
GROUP BY d.agent_id, da.name, da.city
)
,ranked_city as ( SELECT 
    *,
    DENSE_RANK() OVER (
        PARTITION BY city 
        ORDER BY avg_speed_km_per_min DESC
    ) AS city_speed_rank
FROM delivery_Agent_Stat
)

--  q8 
--  Build the Cancellation Profile
,platform_baseline AS (
    -- Your approach fixed: 1 for cancelled, 0 for successful. AVG() now calculates the true percentage!
    SELECT 
        AVG(CASE WHEN status = 'cancelled' THEN 1.0 ELSE 0.0 END) AS overall_avg_rate
    FROM orders
)
,customer_profiles AS (
    -- Step 2: Compute individual order tallies and cancellation rates per customer
    SELECT 
        c.customer_id,
        c.name,
        c.city,
        COUNT(o.order_id) AS total_orders,
        SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
        ROUND(SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(o.order_id), 2) AS cancellation_rate
    FROM customers c  
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name, c.city
    -- Step 3: Only keep customers who have at least one cancellation
    HAVING SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) >= 1
)

,Cancellation_profile as (
SELECT 
    cp.customer_id,
    cp.name,
    cp.city,
    cp.total_orders,
    cp.cancelled_orders,
    cp.cancellation_rate,
    CASE 
        WHEN cp.cancellation_rate > pb.overall_avg_rate THEN 'yes'
        ELSE 'no'
    END AS above_platform_avg
FROM customer_profiles cp
CROSS JOIN platform_baseline pb
ORDER BY cp.cancellation_rate DESC
)

-- Q9 — Cohort Revenue Retention by Signup Month
, cohort_sizes AS (
    -- Step 1: Calculate the total number of unique customers who signed up in each cohort month
    SELECT 
        DATE_FORMAT(signup_date, '%Y-%m') AS cohort,
        COUNT(customer_id) AS cohort_size
    FROM customers
    GROUP BY DATE_FORMAT(signup_date, '%Y-%m')
),
monthly_revenue AS (
    -- Step 2: Track total net spending per customer per active calendar month
    SELECT 
        c.customer_id,
        DATE_FORMAT(c.signup_date, '%Y-%m') AS cohort,
        DATE_FORMAT(o.order_date, '%Y-%m') AS month,
        SUM(o.total_amount - o.discount_applied) AS net_revenue
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_date >= '2024-01-01' AND o.order_date < '2024-04-01'
    GROUP BY c.customer_id, DATE_FORMAT(c.signup_date, '%Y-%m'), DATE_FORMAT(o.order_date, '%Y-%m')
),
cohort_revenue_retention AS (
    -- Step 3: Combine metrics and aggregate final performance values into a CTE
    SELECT 
        mr.cohort,
        mr.month,
        cs.cohort_size,
        ROUND(SUM(mr.net_revenue), 2) AS net_revenue,
        ROUND(SUM(mr.net_revenue) / cs.cohort_size, 2) AS revenue_per_customer
    FROM monthly_revenue mr
    JOIN cohort_sizes cs ON mr.cohort = cs.cohort
    GROUP BY mr.cohort, mr.month, cs.cohort_size
)
-- Step 4: Final Select execution from your master CTE
-- SELECT * 
-- FROM cohort_revenue_retention
-- ORDER BY cohort ASC, month ASC;


-- q 10 
, platform_cancel_baseline AS (
    -- Step 1: Calculate global platform cancellation rate (Q8 prerequisite)
    SELECT AVG(CASE WHEN status = 'cancelled' THEN 1.0 ELSE 0.0 END) AS global_avg_rate
    FROM orders
),
city_revenue_metrics AS (
    -- Step 2: Compute revenue, order volume, and average order values for Jan vs Mar (Q1 & Q2)
    SELECT 
        r.city,
        SUM(CASE WHEN o.order_date >= '2024-01-01' AND o.order_date < '2024-02-01' THEN (o.total_amount - o.discount_applied) ELSE 0 END) AS jan_rev,
        SUM(CASE WHEN o.order_date >= '2024-03-01' AND o.order_date < '2024-04-01' THEN (o.total_amount - o.discount_applied) ELSE 0 END) AS mar_rev,
        COUNT(CASE WHEN o.order_date >= '2024-01-01' AND o.order_date < '2024-02-01' AND o.status = 'delivered' THEN o.order_id END) AS jan_vol,
        COUNT(CASE WHEN o.order_date >= '2024-03-01' AND o.order_date < '2024-04-01' AND o.status = 'delivered' THEN o.order_id END) AS mar_vol,
        AVG(CASE WHEN o.order_date >= '2024-01-01' AND o.order_date < '2024-02-01' AND o.status = 'delivered' THEN (o.total_amount - o.discount_applied) END) AS jan_aov,
        AVG(CASE WHEN o.order_date >= '2024-03-01' AND o.order_date < '2024-04-01' AND o.status = 'delivered' THEN (o.total_amount - o.discount_applied) END) AS mar_aov
    FROM restaurants r
    JOIN orders o ON r.restaurant_id = o.restaurant_id
    WHERE r.city IN ('Delhi', 'Mumbai')
    GROUP BY r.city
)
,restaurant_ranks AS (
    -- Step 3: Find restaurants with Jan orders and 0 March orders, ranked by highest Jan volume (Q4 & Q5)
    SELECT 
        r.city,
        r.name AS restaurant_name,
        ROW_NUMBER() OVER (
            PARTITION BY r.city 
            ORDER BY COUNT(CASE WHEN o.order_date >= '2024-01-01' AND o.order_date < '2024-02-01' THEN o.order_id END) DESC, r.restaurant_id ASC
        ) AS r_rank
    FROM restaurants r
    JOIN orders o ON r.restaurant_id = o.restaurant_id
    GROUP BY r.city, r.restaurant_id, r.name
    HAVING COUNT(CASE WHEN o.order_date >= '2024-01-01' AND o.order_date < '2024-02-01' THEN o.order_id END) > 0
       AND COUNT(CASE WHEN o.order_date >= '2024-03-01' AND o.order_date < '2024-04-01' THEN o.order_id END) = 0
)
,
top_dropped AS (
    -- Step 4: Isolate the #1 dropped restaurant per city
    SELECT city, restaurant_name FROM restaurant_ranks WHERE r_rank = 1
),
agent_speeds AS (
    -- Step 5: Compute average speed for every agent and rank them slowest first per city (Q5/Speedometer)
    SELECT 
        da.city,
        da.name AS agent_name,
        ROW_NUMBER() OVER (
            PARTITION BY da.city 
            ORDER BY AVG(d.distance_km / TIMESTAMPDIFF(MINUTE, d.pickup_time, d.drop_time)) ASC, da.agent_id ASC
        ) AS speed_rank
    FROM deliveries d
    JOIN delivery_agents da ON d.agent_id = da.agent_id
    WHERE d.drop_time > d.pickup_time
    GROUP BY da.city, da.agent_id, da.name
),

slowest_agents AS (
    -- Step 6: Extract the #1 slowest agent per city
    SELECT city, agent_name FROM agent_speeds WHERE speed_rank = 1
),
high_cancel_customers AS (
    -- Step 7: Count customers whose cancellation rate exceeds the platform baseline (Q8)
    SELECT 
        c.city,
        COUNT(DISTINCT c.customer_id) AS bad_cancel_cust_count
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    CROSS JOIN platform_cancel_baseline pcb
    GROUP BY c.city, pcb.global_avg_rate
    HAVING (AVG(CASE WHEN o.status = 'cancelled' THEN 1.0 ELSE 0.0 END)) > pcb.global_avg_rate
)
-- Step 8: Assemble the final unified analytics record per city
SELECT 
    crm.city,
    ROUND(crm.jan_rev, 2) AS jan_net_revenue,
    ROUND(crm.mar_rev, 2) AS mar_net_revenue,
    ROUND(((crm.jan_rev - crm.mar_rev) / crm.jan_rev) * 100, 2) AS revenue_drop_pct,
    CASE 
        WHEN ((crm.jan_vol - crm.mar_vol) / crm.jan_vol) > 0.30 AND ((crm.jan_aov - crm.mar_aov) / crm.jan_aov) > 0.30 THEN 'both'
        WHEN ((crm.jan_vol - crm.mar_vol) / crm.jan_vol) > 0.30 THEN 'volume_drop'
        WHEN ((crm.jan_aov - crm.mar_aov) / crm.jan_aov) > 0.30 THEN 'value_drop'
        ELSE 'other'
    END AS dominant_drop_reason,
    COALESCE(td.restaurant_name, 'None') AS top_dropped_restaurant,
    COALESCE(sa.agent_name, 'None') AS slowest_agent,
    COALESCE(hcc.bad_cancel_cust_count, 0) AS high_cancel_customer_count
FROM city_revenue_metrics crm
LEFT JOIN top_dropped td ON crm.city = td.city
LEFT JOIN slowest_agents sa ON crm.city = sa.city
LEFT JOIN high_cancel_customers hcc ON crm.city = hcc.city;
