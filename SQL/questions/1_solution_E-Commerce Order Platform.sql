-- Create Customers table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(50),
    signup_date DATE
);
-- Create Products table
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(30),
    category VARCHAR(20),
    price DECIMAL(10, 2),
    referred_by INT,
    FOREIGN KEY (referred_by) REFERENCES products(product_id)
);

-- Create Orders table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Create Order_Items table
CREATE TABLE order_items (
    item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    discount INT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Insert data into Customers
INSERT INTO customers VALUES (1, 'Animesh', 'Delhi', '2022-03-15');
INSERT INTO customers VALUES (2, 'Rohit', 'Mumbai', '2022-03-20');
INSERT INTO customers VALUES (3, 'Sneha', 'Delhi', '2023-07-01');
INSERT INTO customers VALUES (4, 'Karan', 'Bangalore', '2021-11-10');

-- Insert data into Products
INSERT INTO products VALUES (1, 'Phone X', 'Electronics', 15000, NULL);
INSERT INTO products VALUES (2, 'Phone Case', 'Accessories', 300, 1);
INSERT INTO products VALUES (3, 'Laptop Pro', 'Electronics', 75000, NULL);
INSERT INTO products VALUES (4, 'USB Hub', 'Accessories', 800, 3);
INSERT INTO products VALUES (5, 'Screen Guard', 'Accessories', 150, 2);
INSERT INTO products VALUES (6, 'Webcam HD', 'Accessories', 90, 5);


-- Insert data into Orders
INSERT INTO orders VALUES (101, 1, '2024-01-10', 'delivered');
INSERT INTO orders VALUES (102, 1, '2024-02-15', 'returned');
INSERT INTO orders VALUES (103, 2, '2024-01-20', 'delivered');
INSERT INTO orders VALUES (104, 3, '2024-03-05', 'pending');
INSERT INTO orders VALUES (105, 1, '2024-04-01', 'delivered');

-- Insert data into Order_Items
INSERT INTO order_items VALUES (1, 101, 1, 1, 10);
INSERT INTO order_items VALUES (2, 101, 2, 2, 0);
INSERT INTO order_items VALUES (3, 102, 3, 1, 5);
INSERT INTO order_items VALUES (4, 103, 1, 1, 0);
INSERT INTO order_items VALUES (5, 104, 4, 3, 15);
INSERT INTO order_items VALUES (6, 105, 5, 5, 0);



with cte as (
select p.product_id ,p.category,p.price,o.quantity,o.discount,
price*quantity*(1-o.discount/100.0) as revenue
from products p 
join order_items o 
on p.product_id=o.product_id
join orders ord 
on o.order_id =ord.order_id
where ord.status ='delivered'
)

select category,sum(revenue) as total_revenue
from cte 
group by category
having sum(revenue) >10000
order by total_revenue desc


, cte2 as (
SELECT p.product_id ,product_name,p.category , sum(o.quantity) AS total_qty
FROM order_items o
JOIN products p ON p.product_id = o.product_id
group by p.product_id,p.product_name,p.category
)

,ranked as (

select *,rank() over (

partition by category order by total_qty desc
) as rnk from cte2
)
select * from ranked
where rnk<=2


select customer_id,order_id,order_date,
DATEDIFF(
day,
lag(order_date) over 
(partition by customer_id order by order_date)
, order_date)

from orders



, cte as (
select p.product_id ,p.category,p.price,o.quantity,o.discount,
price*quantity*(1-o.discount/100.0) as revenue
from products p 
join order_items o 
on p.product_id=o.product_id
)
with   orderrevenue as (
select o.order_id,
sum(price*quantity*(1-o.discount/100.0) )as revenue
from products p
join order_items o
on p.product_id=o.product_id
group by o.order_id
)

select o.customer_id, 
ord.order_id ,
o.order_date,
ord.revenue as order_total,
sum(ord.revenue) over (partition by customer_id order by order_date) as running_total

from orderrevenue ord join 
orders o on ord.order_id=o.order_id

having avg(p.price*ot.quantity*(1-ot.discount/100.0)) >=5000 
and count(o.order_id)>2 

with cte as (
select (o.order_id),o.customer_id,sum(p.price*ot.quantity*(1-ot.discount/100.0))
as order_value
from orders o join order_items ot on o.order_id=ot.order_id
join products p on p.product_id =ot.product_id
group by o.order_id,o.customer_id
)

select customer_id,
count(order_id),
avg(order_value)
from cte 
group by customer_id
having count(order_id)>2
and avg(order_value)>5000


Correlated Subquery

with cte as (
select customer_id,max(order_date) as recent_Date
from orders 
where  status="returned"
group by customer_id
)

select c.customer_id,cu.name
from cte c 
join customers cu 
on c.customer_id=cu.customer_id

select * from orders;


select date_format(order_date,'%Y-%m') as month ,
count(*) as order_count 
from orders
group by date_format(order_date,'%Y-%m') 
order by order_count desc 
limit 1



with customer_revenue as (
select o.customer_id,sum(p.price*ot.quantity*(1-ot.discount/100.0))
as total_spend
from orders o join order_items ot on o.order_id=ot.order_id
join products p on p.product_id =ot.product_id
group by o.customer_id
)

select customer_id,total_spend,
NTILE(4)  over ( order by total_spend) as n 
from customer_revenue 
group by customer_id

select * from customer_revenue


select * from customers;

select c.customer_id,c.city,
c2.customer_id,c2.city
from customers c 
left join customers c2 
on c.city=c2.city
and  c.customer_id < c2.customer_id; 


WITH product_revenue AS (
    SELECT 
        p.product_id, 
        p.product_name,
        SUM(p.price * o.quantity * (1 - o.discount / 100.0)) AS total_revenue
    FROM products p 
    JOIN order_items o ON p.product_id = o.product_id
    GROUP BY p.product_id, p.product_name
)
SELECT *,
    RANK() OVER (ORDER BY total_revenue DESC) AS "rank",
    DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS "dense_rank"
FROM product_revenue;







WITH order_revenue AS (
    SELECT 
        o.order_id, 
        SUM(p.price * o.quantity * (1 - o.discount / 100.0)) AS total_revenue
    FROM products p 
    JOIN order_items o ON p.product_id = o.product_id
    GROUP BY o.order_id
    )
    
    
, order_detail as (
select p.order_id,
p.total_revenue,
o.order_date,
o.customer_id
from order_revenue p 
join orders o on o.order_id=p.order_id

)

select * from (
select customer_id,
order_id,
total_revenue,
row_number() over (partition by customer_id order by order_date) as rn
from order_detail

) a 
where rn =1



SELECT c.customer_id, 
c.name 
FROM customers c 
WHERE exists(
select 1 from orders o 
where o.customer_id=c.customer_id
and o.status="returned"

)




WITH product_revenue AS (
    SELECT 
        p.product_id, 
        p.product_name,
        p.category,
        SUM(p.price * o.quantity * (1 - o.discount / 100.0)) AS total_revenue
    FROM products p 
    JOIN order_items o ON p.product_id = o.product_id
    GROUP BY p.product_id, p.product_name
)

select *,
percent_rank() over (partition by category order by total_revenue DESC) as rn 

from product_revenue


select p.product_id ,o.product_id 
from products p 
left   join order_items o 

on p.product_id =o.product_id




select customer_id
from orders 
group by customer_id
having count(distinct month(order_date))>=1 


select * from order_items;



select o.order_id  ,p.product_name,
o.product_id ,
lead(p.product_name ) over (partition by o.order_id 
order by  o.product_id) as next_order
from order_items o 
join products p 
on o.product_id=p.product_id



WITH order_revenue AS (
    SELECT 
        o.order_id, 
        SUM(p.price * o.quantity * (1- o.discount / 100.0)) AS total_revenue
    FROM products p 
    JOIN order_items o ON p.product_id = o.product_id

    GROUP BY o.order_id
    )
  ,a as(
  select ord.order_date,o.total_revenue
  from order_revenue o 
join orders ord 
on ord.order_id=o.order_id
)

select order_date,total_revenue,
avg(total_revenue) over (

order by order_date
rows between 6 preceding and current row 
) as rolling_Avg


from a 


























































