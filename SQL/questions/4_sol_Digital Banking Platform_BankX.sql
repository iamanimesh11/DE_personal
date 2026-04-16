-- 1. Create Users Table
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    kyc_verified BOOLEAN
);

-- 2. Create Accounts Table
CREATE TABLE accounts (
    account_id VARCHAR(10) PRIMARY KEY,
    user_id INT,
    account_type VARCHAR(20),
    city VARCHAR(50),
    opened_date DATE,
    balance DECIMAL(15, 2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 3. Create Transactions Table
CREATE TABLE transactions (
    txn_id VARCHAR(10) PRIMARY KEY,
    account_id VARCHAR(10),
    txn_type VARCHAR(10), -- 'credit' or 'debit'
    amount DECIMAL(15, 2),
    txn_date DATE,
    status VARCHAR(10), -- 'success' or 'failed'
    merchant VARCHAR(50),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

-- 4. Create Loans Table
CREATE TABLE loans (
    loan_id VARCHAR(10) PRIMARY KEY,
    user_id INT,
    amount DECIMAL(15, 2),
    interest_rate DECIMAL(5, 2),
    start_date DATE,
    end_date DATE,
    status VARCHAR(10), -- 'active' or 'closed'
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


-- 1. Insert Sample Data into Users
INSERT INTO users (user_id, name, age, kyc_verified) VALUES
(1, 'Animesh', 28, true),
(2, 'Rohit', 35, true),
(3, 'Sneha', 24, false),
(4, 'Karan', 31, true),
(5, 'Priya', 27, true);

-- 2. Insert Sample Data into Accounts
INSERT INTO accounts (account_id, user_id, account_type, city, opened_date, balance) VALUES
('A01', 1, 'savings', 'Delhi', '2020-06-01', 15000.00),
('A02', 2, 'current', 'Mumbai', '2019-03-15', 82000.00),
('A03', 3, 'savings', 'Delhi', '2021-09-10', 3200.00),
('A04', 4, 'savings', 'Bangalore', '2022-01-20', 47000.00),
('A05', 5, 'current', 'Mumbai', '2020-11-05', 9500.00);

-- 3. Insert Sample Data into Transactions
INSERT INTO transactions (txn_id, account_id, txn_type, amount, txn_date, status, merchant) VALUES
('T01', 'A01', 'debit', 2000.00, '2024-01-03', 'success', 'Amazon'),
('T02', 'A01', 'credit', 5000.00, '2024-01-10', 'success', 'Salary'),
('T03', 'A02', 'debit', 15000.00, '2024-01-05', 'success', 'HDFC Loan'),
('T04', 'A03', 'debit', 500.00, '2024-01-07', 'failed', 'Swiggy'),
('T05', 'A02', 'credit', 30000.00, '2024-01-15', 'success', 'Client Payment'),
('T06', 'A04', 'debit', 8000.00, '2024-01-18', 'success', 'Flipkart'),
('T07', 'A01', 'debit', 1200.00, '2024-02-02', 'success', 'Zomato'),
('T08', 'A04', 'credit', 20000.00, '2024-02-10', 'success', 'Salary'),
('T09', 'A05', 'debit', 3000.00, '2024-02-14', 'failed', 'Netflix'),
('T10', 'A02', 'debit', 10000.00, '2024-02-20', 'success', 'Rent'),
('T11', 'A01', 'credit', 5000.00, '2024-03-01', 'success', 'Freelance'),
('T12', 'A04', 'debit', 5000.00, '2024-03-05', 'success', 'Amazon'),
('T13', 'A03', 'credit', 1000.00, '2024-03-10', 'failed', 'Transfer'),
('T14', 'A05', 'debit', 2000.00, '2024-03-12', 'success', 'Uber'),
('T15', 'A02', 'credit', 50000.00, '2024-03-20', 'success', 'Client Payment');

-- 4. Insert Sample Data into Loans
INSERT INTO loans (loan_id, user_id, amount, interest_rate, start_date, end_date, status) VALUES
('L01', 1, 100000.00, 8.5, '2022-01-01', '2025-01-01', 'active'),
('L02', 2, 500000.00, 7.2, '2021-06-01', '2026-06-01', 'active'),
('L03', 4, 200000.00, 9.0, '2023-03-01', '2026-03-01', 'active'),
('L04', 3, 50000.00, 12.0, '2023-07-01', '2024-07-01', 'active');


q1 

with cte as (
SELECT 
    account_id,
    txn_id,
    txn_date,
    CASE 
        WHEN DATEDIFF(txn_date, LAG(txn_date) OVER (PARTITION BY account_id ORDER BY txn_date)) > 10 
        THEN 1 
        ELSE 0 
    END AS is_delayed_txn
FROM transactions
)


select account_id,txn_id,
txn_date,
sum(is_delayed_txn) over( PARTITION by account_id ORDER by txn_id)+1
AS
session_id
from cte 



q3


WITH cte AS (
    SELECT 
        account_id,
        txn_date,
        DATE_SUB(txn_date, INTERVAL ROW_NUMBER() OVER (
            PARTITION BY account_id ORDER BY txn_date
        ) DAY) AS adj_date
    FROM transactions
)

SELECT 
    account_id, 
    COUNT(*) AS streak_length,
    MIN(txn_date) AS streak_start,
    MAX(txn_date) AS streak_end
FROM cte 
GROUP BY account_id, adj_date
ORDER BY streak_length DESC;

 q4
 
select * from accounts;
select * from transactions;
 
select a.account_id,a.account_type ,t.amount,
percent_rank() over (PARTITION by a.account_type order by t.amount) as pc 
from accounts a 
join transactions t on a.account_id=t.account_id
where t.status="success"

q5
with cte as (
select account_id,amount ,
PERCENT_RANK() OVER (PARTITION BY account_id ORDER BY amount) AS pct
from transactions

)
SELECT 
    account_id,
    AVG(amount) AS median_balance
FROM cte
-- We look for rows that straddle the 50% mark
WHERE pct <= 0.5 
  OR pct >= 0.5
GROUP BY account_id;

q6

SELECT * from accounts;

select a.account_id as account_1 ,b.account_id as account_2 ,
a.city,a.account_type
from accounts a 
join accounts b 
on a.city=b.city and 
a.account_type=b.account_type
WHERE a.account_id!=b.account_id and
a.account_id<b.account_id

SELECT city, account_type, GROUP_CONCAT(account_id) as accounts
FROM accounts
GROUP BY city, account_type
HAVING COUNT(*) > 1;




q7 
select * from transactions;


select account_id	,txn_id,	txn_date	,amount,
lead(amount) over ( PARTITION by account_id order by txn_date )
as next_amount	,
lead(txn_type) over ( PARTITION by account_id order by txn_date )
as next_type
from transactions


q8

WITH cte AS (
    SELECT 
        account_id,
        MAX(txn_date) AS last_txn_date
    FROM transactions
    GROUP BY account_id
)
SELECT DISTINCT t.account_id, t.last_txn_date
FROM cte t
JOIN transactions t2 
  ON t.account_id = t2.account_id      -- Essential: match the specific account
  AND t.last_txn_date = t2.txn_date    -- match the date
WHERE t2.status = 'failed';

SELECT account_id, txn_date
FROM transactions
WHERE (account_id, txn_date) IN (
    SELECT account_id, MAX(txn_date)
    FROM transactions
    GROUP BY account_id
)
AND status = 'failed';



WITH ranked_txns AS (
    SELECT 
        account_id, 
        status, 
        txn_date,
        RANK() OVER (PARTITION BY account_id ORDER BY txn_date DESC, txn_id DESC) as rnk
    FROM transactions
)
SELECT account_id, txn_date
FROM ranked_txns
WHERE rnk = 1 AND status = 'failed';


-- Q9

select * from accounts;
select * from transactions;

WITH user_spending AS (
    SELECT 
        u.user_id, 
        u.name,
        -- Use COALESCE to show 0 instead of NULL for users with no debits
        COALESCE(SUM(t.amount), 0) AS total_amount 
    FROM users u
    LEFT JOIN accounts a ON u.user_id = a.user_id
    LEFT JOIN transactions t ON a.account_id = t.account_id 
        AND t.status = 'success' 
        AND t.txn_type = 'debit'
    GROUP BY u.user_id, u.name
),
tier_calc AS (
    SELECT 
        *, 
        -- Divide directly into 3 equal groups
        NTILE(3) OVER (ORDER BY total_amount ASC) AS tile
    FROM user_spending
)
SELECT 
    user_id, 
    name, 
    total_amount,
    CASE 
        WHEN tile = 1 THEN 'Low'
        WHEN tile = 2 THEN 'Mid'
        ELSE 'High'
    END AS tier
FROM tier_calc;




q10

SELECT * from transactions;



select account_id,txn_id,txn_date,amount,txn_type,
sum(
case WHEN txn_type="credit" then amount
when txn_type="debit" then -amount
else 0 
end 
) over ( PARTITION by account_id ORDER by txn_date,txn_id)
as running_Balaane
from transactions
where status="success"
ORDER BY account_id, txn_date;


Q11 

select * from accounts;
select * from transactions;

select * from (
select a.city,
SUM(t.amount) as total_volume, 
t.merchant,
rank() over (PARTITION by a.city order by sum(t.amount) desc)as rn 
from accounts a 
join transactions t on 
a.account_id=t.account_id
where t.status="success" and t.txn_type="debit"
    GROUP BY a.city, t.merchant 
) as p





q12
select * from users;
select * from loans;
select * from Transactions;



select u.user_id ,u.name,l.loan_id from users u
join Accounts a
on u.user_id=a.user_id
join Transactions t 
on a.account_id =t.account_id
join loans l 
on u.user_id=l.user_id
where  t.status="failed"
and l.status="active"
GROUP by u.user_id,u.name,l.loan_id

select u.user_id,u.name
from users u 
where exists (
select 1 from loans l 
where l.user_id=u.user_id and l.status="active"
)
and 
exists (
SELECT 1 FROM accounts a
    JOIN transactions t ON a.account_id = t.account_id
    WHERE a.user_id = u.user_id AND t.status = 'failed'

)


Q 13

select * from transactions;

with monthly_Sales as (
select date_format(txn_date,"%Y-%m") as month,

sum(amount) as monthly_sum
from transactions
where status="success"
group by month)

,lagged_data AS (
    SELECT 
        month,
        monthly_sum,
        -- Get the sum from the previous month
        LAG(monthly_sum) OVER (ORDER BY month) AS prev_month_sum
    FROM monthly_sales
)
SELECT 
    month,
    monthly_sum,
    prev_month_sum,
    -- Calculate the percentage change
    ROUND(
        ((monthly_sum - prev_month_sum) / prev_month_sum) * 100, 
        2
    ) AS mom_change_pct
FROM lagged_data;




q14

SELECT account_id,	txn_id, txn_date, amount,
first_value(amount) over (PARTITION by account_id order by txn_date,txn_id) 
as first_txn_amount
FROM transactions 


q15 

select * from transactions;

SELECT 
    account_id, 
    DATE_FORMAT(txn_date, "%Y-%m") AS month,
    -- Sum of money for debits
    SUM(CASE WHEN txn_type = 'debit' THEN amount ELSE 0 END) AS total_debit_amount,
    -- Sum of money for credits
    SUM(CASE WHEN txn_type = 'credit' THEN amount ELSE 0 END) AS total_credit_amount,
    -- Optional: Net change for the month
    SUM(CASE WHEN txn_type = 'credit' THEN amount ELSE -amount END) AS net_cash_flow
FROM transactions 
WHERE status = 'success'
GROUP BY account_id, month
ORDER BY account_id,month ;

Q16 

select account_id	,txn_id	,amount,
lag(amount) over (PARTITION by account_id order by txn_date,txn_id)as prev_amount,
case 
  when amount<0.5*(lag(amount) over (PARTITION by account_id 
                                      order by txn_date,txn_id)
  ) then 1 else 0 
end 
as big_drop
from transactions
where status="success"

Q17


with cte as (
select account_id,
max(txn_date) as  latest_Date
from transactions 
GROUP by account_id
)
,
max_date_indata as  (
select max(txn_date) from transactions
)
select * from cte 
where DATEDIFF(latest_Date,(select max(txn_date) from transactions))>45


q18 

select account_id ,txn_id,txn_date,amount,
avg(amount) over (
PARTITION by account_id order by txn_date,txn_id
rows between 2 preceding  and current row 
) as rolling_avg_3_row
from transactions
where status="success" and account_id="A02"


Q19

select u.user_id	,p.name,
l.Amount as loan_amount	,u.balance,
(l.Amount/u.balance) as burden_ratio,
rank() over (order by (l.Amount/u.balance) ) as rnk 
from accounts u 
join loans l 
on u.user_id=l.user_id
join users p on p.user_id=u.user_id



-- Q20 
select * from transactions;

select merchant,
count(txn_id) as total_transaction,
sum(status="success") as total_successul_transaction,
round((sum(status="success")/count(txn_id))*100,2) as success_rate
from transactions 
GROUP by merchant 
having count(txn_id)>=2
ORDER BY success_rate ASC; 




































































