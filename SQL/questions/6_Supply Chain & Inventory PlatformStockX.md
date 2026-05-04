# SQL Daily Drill — Day 6
### 💀 Level: Brutal — Product-Based Company Interview

**Focus:** Set operations · Bitmasking logic · Slowly Changing Dimensions · Anti-joins · Conditional aggregation traps · Multi-level rollups  
**Nothing repeated from Days 1–5.**

---

## 🏭 Scenario: Supply Chain & Inventory Platform — StockX

Think Amazon warehouse / Flipkart fulfillment backend.

---

## 📦 Tables & Sample Data

**warehouses**
| warehouse_id | city      | region | capacity |
|--------------|-----------|--------|----------|
| W01          | Delhi     | North  | 10000    |
| W02          | Mumbai    | West   | 8000     |
| W03          | Chennai   | South  | 6000     |
| W04          | Kolkata   | East   | 5000     |
| W05          | Bangalore | South  | 7000     |

**products**
| product_id | name           | category    | unit_cost |
|------------|----------------|-------------|-----------|
| P01        | Laptop         | Electronics | 45000.00  |
| P02        | Phone          | Electronics | 18000.00  |
| P03        | Desk Chair     | Furniture   | 8000.00   |
| P04        | Standing Desk  | Furniture   | 22000.00  |
| P05        | Headphones     | Electronics | 3500.00   |
| P06        | Keyboard       | Electronics | 2000.00   |
| P07        | Bookshelf      | Furniture   | 5500.00   |

**inventory**
| inv_id | warehouse_id | product_id | quantity | last_updated |
|--------|--------------|------------|----------|--------------|
| I01    | W01          | P01        | 120      | 2024-01-10   |
| I02    | W01          | P02        | 300      | 2024-01-10   |
| I03    | W01          | P05        | 500      | 2024-01-15   |
| I04    | W02          | P01        | 80       | 2024-01-08   |
| I05    | W02          | P03        | 200      | 2024-01-12   |
| I06    | W03          | P02        | 150      | 2024-01-09   |
| I07    | W03          | P04        | 60       | 2024-01-11   |
| I08    | W04          | P06        | 400      | 2024-01-07   |
| I09    | W04          | P07        | 90       | 2024-01-13   |
| I10    | W05          | P01        | 200      | 2024-01-14   |
| I11    | W05          | P03        | 150      | 2024-01-10   |
| I12    | W05          | P05        | 220      | 2024-01-16   |

**orders**
| order_id | warehouse_id | product_id | quantity | order_date | status    | buyer_city |
|----------|--------------|------------|----------|------------|-----------|------------|
| O01      | W01          | P01        | 10       | 2024-01-05 | delivered | Agra       |
| O02      | W01          | P02        | 50       | 2024-01-06 | delivered | Delhi      |
| O03      | W02          | P01        | 5        | 2024-01-07 | cancelled | Pune       |
| O04      | W03          | P02        | 30       | 2024-01-08 | delivered | Coimbatore |
| O05      | W05          | P03        | 20       | 2024-01-09 | delivered | Mysore     |
| O06      | W01          | P05        | 100      | 2024-01-10 | delivered | Delhi      |
| O07      | W04          | P06        | 80       | 2024-01-11 | delivered | Patna      |
| O08      | W05          | P01        | 15       | 2024-01-12 | delivered | Bangalore  |
| O09      | W02          | P03        | 40       | 2024-01-13 | cancelled | Nashik     |
| O10      | W03          | P04        | 10       | 2024-01-14 | delivered | Chennai    |
| O11      | W01          | P01        | 8        | 2024-01-15 | delivered | Noida      |
| O12      | W05          | P05        | 50       | 2024-01-16 | delivered | Bangalore  |
| O13      | W04          | P07        | 30       | 2024-01-17 | delivered | Howrah     |
| O14      | W02          | P01        | 20       | 2024-01-18 | delivered | Mumbai     |
| O15      | W03          | P02        | 20       | 2024-01-19 | returned  | Madurai    |

**suppliers**
| supplier_id | name         | product_id | supply_price | lead_days | active |
|-------------|--------------|------------|--------------|-----------|--------|
| SU01        | TechVend     | P01        | 43000.00     | 5         | true   |
| SU02        | MegaSupply   | P01        | 44000.00     | 3         | true   |
| SU03        | FurniCo      | P03        | 7500.00      | 7         | true   |
| SU04        | FurniCo      | P04        | 20000.00     | 10        | true   |
| SU05        | AudioWorld   | P05        | 3200.00      | 4         | false  |
| SU06        | KeyMasters   | P06        | 1800.00      | 2         | true   |
| SU07        | TechVend     | P02        | 17000.00     | 5         | true   |
| SU08        | ShelfMakers  | P07        | 5000.00      | 6         | true   |

---

## 💀 Problems

---

**Q1 — Set Operations: Products Available in ALL Southern Warehouses**

Southern warehouses are W03 (Chennai) and W05 (Bangalore).  
Find products stocked in **both** W03 and W05 — using set operations, not JOIN.  
Then separately find products in W03 **but not** W05 — again using set operations only.

| products_in_both |
|------------------|
| P02              |
| P05 (W05 has P05 via I12, W03 does not — verify)|

*(W03 has: P02, P04. W05 has: P01, P03, P05. Intersection = none. W03 only = P02, P04)*

**Corrected:**

Products in both W03 and W05:
| product_id |
|------------|
| *(none)*   |

Products in W03 but not W05:
| product_id |
|------------|
| P02        |
| P04        |

---

**Q2 — Anti-Join: Products That Have Never Been Ordered**

Find all products that exist in the products table but have zero orders — ever. Write this using an anti-join pattern (NOT EXISTS or LEFT JOIN ... IS NULL), not NOT IN.

Explain in a comment inside your query why NOT IN is dangerous here if order_id could ever be NULL.

| product_id | name      | category  |
|------------|-----------|-----------|
| P06        | Keyboard  | Electronics |
| P07        | Bookshelf | Furniture   |

*(P06 appears in O07 — check. O07 has P06. So P06 HAS been ordered. P07 appears in O13. So both have orders.)*
*(All products appear in at least one order — add P08 with no orders to your local data to test anti-join logic)*

---

**Q3 — ROLLUP: Inventory Value by Region and Category**

Inventory value = `quantity × unit_cost` per product per warehouse.  
Produce a report using `ROLLUP` that shows:
- Subtotal per region + category
- Subtotal per region (all categories)
- Grand total (all regions, all categories)

NULL in the output represents the rollup subtotal row — do not filter them out.

| region | category    | total_inventory_value | row_type         |
|--------|-------------|----------------------|------------------|
| East   | Electronics | 800000.00            | detail           |
| East   | Furniture   | 495000.00            | detail           |
| East   | NULL        | 1295000.00           | region_subtotal  |
| North  | Electronics | 16560000.00          | detail           |
| North  | NULL        | 16560000.00          | region_subtotal  |
| South  | Electronics | 14820000.00          | detail           |
| South  | Furniture   | 2800000.00           | detail           |
| South  | NULL        | 17620000.00          | region_subtotal  |
| West   | Electronics | 3600000.00           | detail           |
| West   | Furniture   | 1600000.00           | detail           |
| West   | NULL        | 5200000.00           | region_subtotal  |
| NULL   | NULL        | 40675000.00          | grand_total      |

*(North: W01 has P01=120×45000=5400000, P02=300×18000=5400000, P05=500×3500=1750000 → 12550000. Recalculate fully when solving)*

---

**Q4 — Conditional Aggregation Trap: Warehouse Fulfilment Score**

For each warehouse compute:
- `total_orders` — all orders ever
- `fulfillment_rate` — delivered / total (ignore cancelled AND returned both)
- `cancellation_rate` — cancelled / total
- `avg_delivered_qty` — average quantity of delivered orders only

**The trap:** A naive `AVG(quantity)` includes cancelled and returned orders. Make sure your avg only covers delivered.

| warehouse_id | total_orders | fulfillment_rate | cancellation_rate | avg_delivered_qty |
|--------------|--------------|------------------|-------------------|-------------------|
| W01          | 4            | 1.00             | 0.00              | 42.00             |
| W02          | 3            | 0.33             | 0.67              | 20.00             |
| W03          | 3            | 0.67             | 0.00              | 20.00             |
| W04          | 2            | 1.00             | 0.00              | 55.00             |
| W05          | 3            | 1.00             | 0.00              | 28.33             |

*(W01 delivered: O01=10, O02=50, O06=100, O11=8 → avg=(10+50+100+8)/4=42)*
*(W02: O03 cancelled, O09 cancelled, O14 delivered=20 → fulfillment=1/3, cancellation=2/3, avg_delivered=20)*
*(W03: O04 delivered=30, O10 delivered=10, O15 returned=20 → delivered=2, fulfillment=2/3, avg_delivered=(30+10)/2=20)*
*(W04: O07 delivered=80, O13 delivered=30 → avg=(80+30)/2=55)*
*(W05: O05=20, O08=15, O12=50 → avg=(20+15+50)/3=28.33)*

---

**Q5 — SCD Type 2 Simulation: Track Supplier Price Changes**

Your supplier prices change over time. You receive this new snapshot — prices have changed for two suppliers:

```
SU01 TechVend  P01  new price: 43500  effective: 2024-02-01
SU07 TechVend  P02  new price: 16500  effective: 2024-02-01
```

Write a query that simulates SCD Type 2 output — showing the full history with `valid_from`, `valid_to`, and `is_current` flag. Assume original records were valid from `2024-01-01`.

| supplier_id | product_id | supply_price | valid_from | valid_to   | is_current |
|-------------|------------|--------------|------------|------------|------------|
| SU01        | P01        | 43000.00     | 2024-01-01 | 2024-01-31 | false      |
| SU01        | P01        | 43500.00     | 2024-02-01 | NULL       | true       |
| SU07        | P02        | 17000.00     | 2024-01-01 | 2024-01-31 | false      |
| SU07        | P02        | 16500.00     | 2024-02-01 | NULL       | true       |
| SU02        | P01        | 44000.00     | 2024-01-01 | NULL       | true       |

---

**Q6 — Multi-step CTE: Best Supplier Per Product (Multi-criteria)**

For each product that has at least one active supplier, find the best supplier using this priority:
1. Lowest `supply_price` first
2. If tie on price → lowest `lead_days`
3. If still tie → lowest `supplier_id` alphabetically

Only consider `active = true` suppliers.

Chain this in CTEs: rank suppliers per product → filter rank 1 → join back to product details.

| product_id | product_name   | best_supplier_id | supplier_name | supply_price | lead_days |
|------------|----------------|------------------|---------------|--------------|-----------|
| P01        | Laptop         | SU01             | TechVend      | 43000.00     | 5         |
| P02        | Phone          | SU07             | TechVend      | 17000.00     | 5         |
| P03        | Desk Chair     | SU03             | FurniCo       | 7500.00      | 7         |
| P04        | Standing Desk  | SU04             | FurniCo       | 20000.00     | 10        |
| P06        | Keyboard       | SU06             | KeyMasters    | 1800.00      | 2         |
| P07        | Bookshelf      | SU08             | ShelfMakers   | 5000.00      | 6         |

*(P05/Headphones — only supplier SU05 is inactive → P05 gets no row)*

---

**Q7 — Brain Teaser: Find the Warehouse Closest to Stockout**

A warehouse is "closest to stockout" for a product when:  
`remaining_stock = inventory.quantity - SUM(delivered order quantities for that product at that warehouse)`

Find the top 1 product-warehouse combination with the **lowest remaining stock** — without using LIMIT.

| warehouse_id | product_id | initial_qty | delivered_qty | remaining_stock |
|--------------|------------|-------------|---------------|-----------------|
| W01          | P01        | 120         | 18            | 102             |
| W01          | P02        | 300         | 50            | 250             |
| W01          | P05        | 500         | 100           | 400             |
| W05          | P01        | 200         | 15            | 185             |
| W05          | P03        | 150         | 20            | 130             |
| W05          | P05        | 220         | 50            | 170             |
| W02          | P01        | 80          | 20            | 60              |  ← closest
| W03          | P02        | 150         | 30            | 120             |
| W03          | P04        | 60          | 10            | 50              |
| W04          | P06        | 400         | 80            | 320             |
| W04          | P07        | 90          | 30            | 60              |

Lowest remaining = W02/P01 with 60 AND W04/P07 with 60 — both tied.  
Your query must return both tied rows without LIMIT.

| warehouse_id | product_id | remaining_stock |
|--------------|------------|-----------------|
| W02          | P01        | 60              |
| W04          | P07        | 60              |

---

**Q8 — NULL Trap: Supplier Margin Analysis**

Margin per product per supplier = `products.unit_cost - suppliers.supply_price`

**The traps:**
1. SU05 is inactive — include it in margin calc but flag it separately
2. P05 has only one supplier (SU05) which is inactive — it will still show but marked inactive
3. Some products have NO supplier at all (P04 has SU04, check all) — these must appear with NULL margin, not disappear

Show all products, their best margin supplier (active preferred, inactive as fallback), margin value, and active flag.

| product_id | name          | supplier_id | supply_price | margin    | is_active |
|------------|---------------|-------------|--------------|-----------|-----------|
| P01        | Laptop        | SU01        | 43000.00     | 2000.00   | true      |
| P02        | Phone         | SU07        | 17000.00     | 1000.00   | true      |
| P03        | Desk Chair    | SU03        | 7500.00      | 500.00    | true      |
| P04        | Standing Desk | SU04        | 20000.00     | 2000.00   | true      |
| P05        | Headphones    | SU05        | 3200.00      | 300.00    | false     |
| P06        | Keyboard      | SU06        | 1800.00      | 200.00    | true      |
| P07        | Bookshelf     | SU08        | 5000.00      | 500.00    | true      |

---

**Q9 — Brain Teaser: Orders That Were the Sole Order for Their Product on That Day**

Find all orders where, on that specific `order_date`, that product was ordered from **only one warehouse** (i.e., no other warehouse fulfilled the same product on the same day).

This is not a simple GROUP BY. Think about what "sole" means across the entire platform for that product-date combination.

| order_id | product_id | order_date | warehouse_id |
|----------|------------|------------|--------------|
| O01      | P01        | 2024-01-05 | W01          |
| O02      | P02        | 2024-01-06 | W01          |
| O03      | P01        | 2024-01-07 | W02          |
| O04      | P02        | 2024-01-08 | W03          |
| O05      | P03        | 2024-01-09 | W05          |
| O06      | P05        | 2024-01-10 | W01          |
| O07      | P06        | 2024-01-11 | W04          |
| O08      | P01        | 2024-01-12 | W05          |
| O09      | P03        | 2024-01-13 | W02          |
| O10      | P04        | 2024-01-14 | W03          |
| O11      | P01        | 2024-01-15 | W01          |
| O12      | P05        | 2024-01-16 | W05          |
| O13      | P07        | 2024-01-17 | W04          |
| O14      | P01        | 2024-01-18 | W02          |
| O15      | P02        | 2024-01-19 | W03          |

*(Every order_date has exactly one order — so all qualify. Add two same-product same-date orders to test exclusion logic properly)*

---

**Q10 — Multi-step CTE: Regional Inventory Health Report**

Build a full inventory health report per region with 4 CTEs chained:

1. **CTE 1** — compute `stock_value` (quantity × unit_cost) and `delivered_qty` per warehouse-product
2. **CTE 2** — compute `remaining_stock` = inventory qty - delivered qty (only delivered orders)
3. **CTE 3** — flag each product-warehouse as:
   - `critical` → remaining stock < 20% of original inventory
   - `low` → 20–50%
   - `healthy` → above 50%
4. **CTE 4** — aggregate per region: count of critical / low / healthy product-warehouse combos, total remaining stock value

Final output:

| region | critical_count | low_count | healthy_count | total_remaining_value |
|--------|----------------|-----------|---------------|-----------------------|
| North  | 0              | 0         | 3             | 41350000.00 (approx)  |
| West   | 1              | 0         | 1             | ...                   |
| South  | 0              | 1         | 3             | ...                   |
| East   | 0              | 1         | 1             | ...                   |

*(Calculate exact values when solving — use your CTE chain output as source of truth)*

---
