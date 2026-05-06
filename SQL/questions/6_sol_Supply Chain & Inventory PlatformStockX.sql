-- 1. Create Tables
CREATE TABLE warehouses (
    warehouse_id VARCHAR(10) PRIMARY KEY,
    city VARCHAR(50),
    region VARCHAR(50),
    capacity INT
);

CREATE TABLE products (
    product_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    unit_cost DECIMAL(10, 2)
);

CREATE TABLE inventory (
    inv_id VARCHAR(10) PRIMARY KEY,
    warehouse_id VARCHAR(10),
    product_id VARCHAR(10),
    quantity INT,
    last_updated DATE,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE orders (
    order_id VARCHAR(10) PRIMARY KEY,
    warehouse_id VARCHAR(10),
    product_id VARCHAR(10),
    quantity INT,
    order_date DATE,
    status VARCHAR(20),
    buyer_city VARCHAR(50),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE suppliers (
    supplier_id VARCHAR(10),
    name VARCHAR(100),
    product_id VARCHAR(10),
    supply_price DECIMAL(10, 2),
    lead_days INT,
    active BOOLEAN,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 2. Insert Data
INSERT INTO warehouses VALUES 
('W01', 'Delhi', 'North', 10000),
('W02', 'Mumbai', 'West', 8000),
('W03', 'Chennai', 'South', 6000),
('W04', 'Kolkata', 'East', 5000),
('W05', 'Bangalore', 'South', 7000);

INSERT INTO products VALUES 
('P01', 'Laptop', 'Electronics', 45000.00),
('P02', 'Phone', 'Electronics', 18000.00),
('P03', 'Desk Chair', 'Furniture', 8000.00),
('P04', 'Standing Desk', 'Furniture', 22000.00),
('P05', 'Headphones', 'Electronics', 3500.00),
('P06', 'Keyboard', 'Electronics', 2000.00),
('P07', 'Bookshelf', 'Furniture', 5500.00);

INSERT INTO inventory VALUES 
('I01', 'W01', 'P01', 120, '2024-01-10'),
('I02', 'W01', 'P02', 300, '2024-01-10'),
('I03', 'W01', 'P05', 500, '2024-01-15'),
('I04', 'W02', 'P01', 80, '2024-01-08'),
('I05', 'W02', 'P03', 200, '2024-01-12'),
('I06', 'W03', 'P02', 150, '2024-01-09'),
('I07', 'W03', 'P04', 60, '2024-01-11'),
('I08', 'W04', 'P06', 400, '2024-01-07'),
('I09', 'W04', 'P07', 90, '2024-01-13'),
('I10', 'W05', 'P01', 200, '2024-01-14'),
('I11', 'W05', 'P03', 150, '2024-01-10'),
('I12', 'W05', 'P05', 220, '2024-01-16');

INSERT INTO orders VALUES 
('O01', 'W01', 'P01', 10, '2024-01-05', 'delivered', 'Agra'),
('O02', 'W01', 'P02', 50, '2024-01-06', 'delivered', 'Delhi'),
('O03', 'W02', 'P01', 5, '2024-01-07', 'cancelled', 'Pune'),
('O04', 'W03', 'P02', 30, '2024-01-08', 'delivered', 'Coimbatore'),
('O05', 'W05', 'P03', 20, '2024-01-09', 'delivered', 'Mysore'),
('O06', 'W01', 'P05', 100, '2024-01-10', 'delivered', 'Delhi'),
('O07', 'W04', 'P06', 80, '2024-01-11', 'delivered', 'Patna'),
('O08', 'W05', 'P01', 15, '2024-01-12', 'delivered', 'Bangalore'),
('O09', 'W02', 'P03', 40, '2024-01-13', 'cancelled', 'Nashik'),
('O10', 'W03', 'P04', 10, '2024-01-14', 'delivered', 'Chennai'),
('O11', 'W01', 'P01', 8, '2024-01-15', 'delivered', 'Noida'),
('O12', 'W05', 'P05', 50, '2024-01-16', 'delivered', 'Bangalore'),
-- ('O13', 'W04', 'P07', 30, '2024-01-17', 'delivered', 'Howrah'),
('O14', 'W02', 'P01', 20, '2024-01-18', 'delivered', 'Mumbai'),
('O15', 'W03', 'P02', 20, '2024-01-19', 'returned', 'Madurai');

INSERT INTO suppliers VALUES 
('SU01', 'TechVend', 'P01', 43000.00, 5, true),
('SU02', 'MegaSupply', 'P01', 44000.00, 3, true),
('SU03', 'FurniCo', 'P03', 7500.00, 7, true),
('SU04', 'FurniCo', 'P04', 20000.00, 10, true),
('SU05', 'AudioWorld', 'P05', 3200.00, 4, false),
('SU06', 'KeyMasters', 'P06', 1800.00, 2, true),
('SU07', 'TechVend', 'P02', 17000.00, 5, true),
('SU08', 'ShelfMakers', 'P07', 5000.00, 6, true);


-- product in both W03 AND W05 
SELECT product_id FROM inventory WHERE warehouse_id = 'W03'
INTERSECT
SELECT product_id FROM inventory WHERE warehouse_id = 'W05';

-- prodcut in wo3 not in wo5 :

SELECT product_id FROM inventory WHERE warehouse_id = 'W03'
EXCEPT
SELECT product_id FROM inventory WHERE warehouse_id = 'W05';




-- product which neve rordered

-- SELECT 
--     p.product_id, 
--     p.name, 
--     p.category
-- FROM products p
-- LEFT JOIN orders o ON p.product_id = o.product_id
-- WHERE o.product_id IS NULL;


-- -- 
-- -- Subtotal per Region + Category
-- -- SELECT w.region, p.category, SUM(i.quantity * p.unit_cost) AS total_value
-- -- FROM inventory i
-- -- JOIN products p ON i.product_id = p.product_id
-- -- JOIN warehouses w ON i.warehouse_id = w.warehouse_id
-- -- GROUP BY w.region, p.category

-- -- SELECT w.region, NULL, SUM(i.quantity * p.unit_cost)
-- -- FROM inventory i
-- -- JOIN products p ON i.product_id = p.product_id
-- -- JOIN warehouses w ON i.warehouse_id = w.warehouse_id
-- -- GROUP BY w.region


-- -- 3. Grand Total (All Regions, All Categories)
-- -- SELECT NULL, NULL, SUM(i.quantity * p.unit_cost)
-- -- FROM inventory i
-- -- JOIN products p ON i.product_id = p.product_id;


-- SELECT 
--     COALESCE(w.region, 'GRAND TOTAL') AS region, 
--     COALESCE(p.category, 'All Categories') AS category, 
--     SUM(i.quantity * p.unit_cost) AS total_inventory_value
-- FROM inventory i
-- JOIN products p ON i.product_id = p.product_id
-- JOIN warehouses w ON i.warehouse_id = w.warehouse_id
-- GROUP BY ROLLUP (w.region, p.category);




-- -- 1. Subtotal per Region + Category
-- SELECT w.region, p.category, SUM(i.quantity * p.unit_cost) AS total_value
-- FROM inventory i
-- JOIN products p ON i.product_id = p.product_id
-- JOIN warehouses w ON i.warehouse_id = w.warehouse_id
-- GROUP BY w.region, p.category

-- UNION ALL

-- -- 2. Subtotal per Region (All Categories)
-- SELECT w.region, NULL, SUM(i.quantity * p.unit_cost)
-- FROM inventory i
-- JOIN products p ON i.product_id = p.product_id
-- JOIN warehouses w ON i.warehouse_id = w.warehouse_id
-- GROUP BY w.region

-- UNION ALL

-- -- 3. Grand Total (All Regions, All Categories)
-- SELECT NULL, NULL, SUM(i.quantity * p.unit_cost)
-- FROM inventory i
-- JOIN products p ON i.product_id = p.product_id;



-- Q4

-- select w.warehouse_id,
-- count(*) as Total_orders,
-- sum(case when o.status="delivered" then 1 else 0 end)/count(*) as fullfilment_Rate,
-- sum(case when o.status="cancelled" then 1 else 0 end)/count(*) as cancelled_Rate,
-- avg(case when o.status="delivered"then o.quantity else NULL end)as avg_delivered_qty 
-- from warehouses w 
-- join orders o on w.warehouse_id=o.warehouse_id
-- GROUP by w.warehouse_id




-- Q5 — SCD Type 2 Simulation: Track Supplier Price Changes
-- WITH CombinedSource AS (
--     -- 1. Grab original data and assign the assumed start date
--     SELECT 
--         supplier_id, 
--         name, 
--         product_id, 
--         supply_price, 
--         '2024-01-01' AS valid_from
--     FROM suppliers
    
--     UNION ALL
    
--     -- 2. Add the new updates with their effective date
--     SELECT 'SU01', 'TechVend', 'P01', 43500, '2024-02-01'
--     UNION ALL
--     SELECT 'SU07', 'TechVend', 'P02', 16500, '2024-02-01'
-- )
-- ,
-- HistoryLogic AS (
--     SELECT 
--         *,
--         -- Look at the next row's start date to close the current row
--         LEAD(valid_from) OVER (
--             PARTITION BY supplier_id, product_id 
--             ORDER BY valid_from
--         ) AS next_valid_from
--     FROM CombinedSource
-- )

-- SELECT 
--     supplier_id,
--     name,
--     product_id,
--     supply_price,
--     valid_from,
--     -- If there's no next date, the price is still active
--     COALESCE(next_valid_from,'NULL') AS valid_to,
--     -- If there's no next date, it's the current record
--     CASE WHEN next_valid_from IS NULL THEN 1 ELSE 0 END AS is_current
-- FROM HistoryLogic
-- ORDER BY supplier_id, valid_from;


-- Q6 — Multi-step CTE: Best Supplier Per Product (Multi-criteria)



-- with RankedSuppliers AS (
--     SELECT 
--         product_id,
--         supplier_id,
--         supply_price,
--         lead_days,
--         -- Priority 1: Price, Priority 2: Lead Days, Priority 3: ID
--         ROW_NUMBER() OVER (
--             PARTITION BY product_id 
--             ORDER BY supply_price ASC, lead_days ASC, supplier_id ASC
--         ) AS rn 
--     FROM suppliers
--     where active=1
-- )

-- select * from RankedSuppliers
-- where rn=1 


-- q7 
--   select * from orders;
  
--   with cte as (
--   select o.warehouse_id,o.product_id,
--   sum(o.quantity) as total_quantity
--   from orders o 
--   where o.status="delivered"
--   GROUP by o.warehouse_id,o.product_id
-- )

-- select 
-- c.warehouse_id,
-- c.product_id,
-- i.quantity as intialquantity,
-- c.total_quantity,
-- i.quantity- c.total_quantity as remaining_stock,
-- rank() over (
-- order by (i.quantity- c.total_quantity)) as rn 
-- from cte  c 
-- join inventory i 
-- on c.warehouse_id=i.warehouse_id and c.product_id=i.product_id


-- q8 
-- select * from (
-- select p.product_id,p.name,
-- s.supplier_id,s.supply_price,
-- p.unit_cost- s.supply_price as margin,
--         s.active, 
-- ROW_NUMBER() over (
--         PARTITION by product_id 
--         order by  s.active desc , (p.unit_cost- s.supply_price) desc
--         ) as rn 
-- from products p
-- left join suppliers s 
-- on p.product_id=s.product_id

-- ) a 
-- where rn =1



-- q9 

-- select * from orders ;

-- with ProductDateWarehouseCount as (
-- select order_date,product_id,
-- count(distinct warehouse_id) as unique_warehouse_count
-- from orders 
-- GROUP by order_date,product_id
-- )


-- SELECT 
--     o.order_id, 
--     o.product_id, 
--     o.order_date, 
--     o.warehouse_id
-- FROM orders o
-- JOIN ProductDateWarehouseCount pdw
--     ON o.order_date = pdw.order_date 
--     AND o.product_id = pdw.product_id
-- WHERE pdw.unique_warehouse_count = 1;

-- with stock_value as (
-- select p.product_id,i.warehouse_id,
-- i.quantity as initial_qty,
-- p.unit_cost,
-- i.quantity * p.unit_cost as stock_value
-- from inventory i 
-- join products p 
-- on p.product_id=i.product_id
-- )
-- , delivered_qty as (
--     select 
--         o.warehouse_id,
--         o.product_id,
--         p.unit_cost,
--         sum(quantity) as total_delivered, -- Summing the actual units
--         sum(quantity * unit_cost) as total_delivered_value -- Optional: total value sold
--     from orders o
--     join products p on o.product_id = p.product_id
--     where o.status = 'delivered'
--     group by o.warehouse_id, o.product_id
-- )
-- ,
-- final as (
-- select s.warehouse_id,
-- s.product_id,
-- s.initial_qty,
-- s.unit_cost,
-- COALESCE(d.total_delivered,0) as delivered_qty,
-- (s.initial_qty- COALESCE(d.total_delivered,0)) as remaining_stock
-- from stock_value s 
-- left join delivered_qty d 
-- on s.warehouse_id=d.warehouse_id
-- and s.product_id=d.product_id
-- )
-- ,
-- remaining_calc  as (
-- select *,
-- (initial_qty- delivered_qty)*1.0 / initial_qty as remaining_pct 
-- from final
--   )
-- ,status as  (
-- SELECT 
--     r.warehouse_id,
--     r.product_id,
--     r.remaining_stock,
--     w.region,
--     (r.remaining_stock * r.unit_cost) AS remaining_stock_value, -- Added for financial analysis
--     CASE 
--         WHEN r.remaining_pct < 0.20 THEN 'critical'
--         WHEN r.remaining_pct BETWEEN 0.20 AND 0.50 THEN 'low'
--         ELSE 'healthy'
--     END AS stock_status
-- FROM remaining_calc r 
-- join warehouses w
-- on r.warehouse_id=w.warehouse_id
-- )

-- select region,
-- sum(case when stock_status="critical" then 1 else 0 end )as critical_count,
-- sum(case when stock_status="low" then 1 else 0 end )as low,
-- sum(case when stock_status="healthy" then 1 else 0 end )as healthy_count,
-- sum(remaining_stock_value) as total_remaining_value
-- from status
-- group by region






WITH CTE1_Base AS (
    -- Compute base values: stock value and total delivered units
    SELECT 
        i.warehouse_id,
        i.product_id,
        i.quantity AS original_qty,
        p.unit_cost,
        (i.quantity * p.unit_cost) AS original_stock_value,
        COALESCE(SUM(CASE WHEN o.status = 'delivered' THEN o.quantity END), 0) AS total_delivered_qty
    FROM inventory i
    JOIN products p ON i.product_id = p.product_id
    LEFT JOIN orders o ON i.warehouse_id = o.warehouse_id AND i.product_id = o.product_id
    GROUP BY i.warehouse_id, i.product_id, i.quantity, p.unit_cost
),

CTE2_Remaining AS (
    -- Compute current stock levels
    SELECT 
        *,
        (original_qty - total_delivered_qty) AS remaining_stock
    FROM CTE1_Base
),

CTE3_Flagging AS (
    -- Categorize stock health based on percentage of original inventory
    SELECT 
        r.*,
        w.region,
        (remaining_stock * unit_cost) AS remaining_stock_value,
        CASE 
            WHEN (remaining_stock * 1.0 / NULLIF(original_qty, 0)) < 0.20 THEN 'critical'
            WHEN (remaining_stock * 1.0 / NULLIF(original_qty, 0)) BETWEEN 0.20 AND 0.50 THEN 'low'
            ELSE 'healthy'
        END AS health_status
    FROM CTE2_Remaining r
    JOIN warehouses w ON r.warehouse_id = w.warehouse_id
),

CTE4_RegionalAggregate AS (
    -- Final aggregation to regional levels
    SELECT 
        region,
        SUM(CASE WHEN health_status = 'critical' THEN 1 ELSE 0 END) AS critical_count,
        SUM(CASE WHEN health_status = 'low' THEN 1 ELSE 0 END) AS low_count,
        SUM(CASE WHEN health_status = 'healthy' THEN 1 ELSE 0 END) AS healthy_count,
        SUM(remaining_stock_value) AS total_remaining_value
    FROM CTE3_Flagging
    GROUP BY region
)

SELECT * FROM CTE4_RegionalAggregate
ORDER BY region;

































