# Amazon Athena — Notes

Amazon Athena is a **serverless, interactive query service** that allows you to query data **directly in Amazon S3 using SQL**, without managing any servers.

---

## ❓ Why Use Athena?

- Data already exists in **Amazon S3**
- Loading data into **Redshift** or **RDS**:
  - Takes time
  - Increases cost

---

## 🌲 Solution: Athena

- Query data **in place** (directly from S3)
- **No ETL required** for data exploration
- Uses **AWS Glue Data Catalog** for table metadata
- Query results can be **stored back in S3**

---

## ⚠️ Limitations

- Athena **cannot query databases directly**, such as:
  - Amazon RDS
  - Amazon DynamoDB
- Data **must exist in S3**

---

## 💰 Pricing

- Pricing is based on **data scanned per query**
- **Query optimization is mandatory** to reduce cost

---

## 🚀 Performance & Optimization

- Athena scans **only required columns**
- Uses **partition pruning**:
  - Only matching partitions are scanned
- **Columnar formats** (Parquet, ORC):
  - Scans only required columns
- **Row-based formats** (CSV, JSON):
  - Entire file is scanned even if only one column is selected

---

## 📊 Athena Tables

- Tables are **external tables**
- Store **metadata only**
- Deleting a table **does not delete the underlying data** in S3



# CTAS (CREATE TABLE AS SELECT)

CTAS is used for:
- Transforming data
- Converting data formats
- Creating analytics-ready tables

---

## 🧪 CTAS Example
```sql
CREATE TABLE sales_parquet
WITH (
  format = 'PARQUET',
  partitioned_by = ARRAY['year']
) AS
SELECT
  *,
  year(order_date) AS year
FROM sales_raw;
```
if not given location to store,it  stor defaut to s3://aws-athena-query-results-<account>/

## 💰 Athena Cost Model

- Athena pricing depends on **data scanned per query**
- Cost is **not based on**:
- Number of rows
- Query execution time
- Proper partitioning and columnar formats reduce cost 🤑
  
## ⚠️ Partition Pruning Failure
when column like year is int but passed a string in query so type mismatch and make athena scan all partition

athena read compression data directly already.


creating a partitioning table(static)
```sql
create external table sales (
id INT,name String,sales INT )
partitioned by (year INT)
STORED AS PARQUET
LOCATION 's3://sales-data/';
```
⚠️ This doesn register partitions

registering partitions
-manual:(not sclaable)
```sql
alter table sales
and patition (year=2024)
location 's3://sales-data/year=2024/';
```

another option: MSCK REPAIR TABLE
```
MSCK REPAIR TABLE SALES;
```
IT SCAN S3 FOLDER STRUCTRE and auto register partitions in glue,
uses for data arrive daily and folder are auto created
its cost heavy for large datasets
so best practice is using incremenatal adds for very karge tables.

means just adding a single partition ,

like new data rrives for : `s3://sales-data/year=2025/month/01/`
and so running 
```sql
ALTER TABLE sales ADD PARTITION (year =2025 ,month=1)
LOCATION 's3://sales-data/year=2025/month/01/';
```

---

 ⭐ ATHENA VS GLUE VS REDSHIFT VS REDSHIFT SPECTRUM

 Question is all about depend on where does the data live and what do i want to do with it ?
 

Service	  |      Description                | Data Location   |
----------|---------------------------------|-----------------|
|ATHENA  	|   Serverless SQL on S3          | S3 only         |
|Glue     |	  ETL  ENGINE                   | S3 ->S3(ETL)    |
|Redshift |	  Data warehouse (stores data)  | Inside Redshift |
|Spectrum	|   Redshift querying S3          | S3+redshift     |


## When data exists only in S3 and you want to run SQL on it

**Use:** ✅ **Amazon Athena**  
- No servers  
- No loading  
- Just SQL directly on S3  

> **Athena = read-only analytics on S3**
! Athena =read only analytics on s3

## case : when change in data requires(ETL)like clearning,joining multiple data,apply python logic,build pipelines
If transformation is:
- Simple SQL → Athena CTAS
- Complex logic / Python / Spark → AWS Glue


| Service | Role         |
|--------|--------------|
| Athena | Query data   |
| Glue   | Process data |

---

Now case if business wants dashboards:
Problem: athen query are slow for dashboard,multipl user hittig queries and need faster response.
Question:

👉 Should dashboards query S3 directly?
❌ No.
Answer:✅ Amazon Redshift
Why?
Stores data internally
Optimized for BI
Handles concurrency
👉 Redshift = final analytics layer

Now You Have BOTH Redshift AND S3 Data
Situation:
Old data already loaded in Redshift
New data still in S3
You want to JOIN them
Question:👉 Do I move S3 data into Redshift?
❌ Not always.
Answer:✅ Redshift Spectrum
Why?
Query S3 from Redshift
No data movement
Unified SQL
👉 Spectrum = Redshift’s eyes into S3

**Note** : 

RAW DATA (S3)
   |
   |---> Athena (explore)
   |
   |---> Glue (transform)
   |
   v
ANALYTICS READY (Parquet in S3)
   |
   |---> Athena (cheap analysis)
   |
   v
WAREHOUSE (Redshift)
   |
   |---> Spectrum (query leftover S3)


Athena → Read S3
Glue → Change S3
Redshift → Store & serve analytics
Spectrum → Redshift reading S3
\


🔹Athena Core Topic  Security, IAM & Lake Formation (EXAM-MANDATORY)

security is enforced via s3+Glue+IAM,athena doesn't has data.

Three layer of security
🔐 Layer 1: IAM(who can query)
who can run athena queries ,can access workgroups.
example: athena:StartQueryExecution,athena:GetQueryResults
📌 Exam line:
IAM controls query execution, not data access

🔐 Layer 2: S3 (What data can be read?)
Which buckets Athena can read,Where query results can be written
Required permissions: s3:GetObject (source data),s3:PutObject (query results)
❌ Missing result bucket permission = query fails

🔐 Layer 3: Glue Data Catalog (What tables exist?)
Database visibility,Table access,Schema visibility
Permissions:,glue:GetDatabase,glue:GetTable

Athena workgroups(cost+Security)
it allow separate users/team,s3 result bucket ,queryy limits

| Requirement              | Use            |
| ------------------------ | -------------- |
| Who can query Athena     | IAM            |
| Which S3 data accessible | S3 policy      |
| Which tables visible     | Glue           |
| Column/row level access  | Lake Formation |
| Cost control             | Workgroups     |
