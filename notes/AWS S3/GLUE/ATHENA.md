# amazon athena -notes
serverless interactive query service that makes query data direclty in s3 using sql without managing servers.
❓ why:
data is already in s3 and loading into redshift /rds cost time and money 
🌲solution :athena -query in place ,no etl requried for exploration
athena runs on glue data catalog table and results can be stored back in S3
⚠️athena cannot query databases direclty like rds ,dynamodb ,data must exist in S3.

pricing :
athena pricing is based on 💰data scennaed per query,optimization is mandatory

athen ause column only ,only partition matched ,entire file if not columnar like in parquet scan only spcific column rather than whole file like csv.

athena table are :
external table
metadata only 
deleting daa does not delete data


## CTAS (Create table as select
used for :
transforming data
converting format
creating analytics ready tables
```sql
create table sales_parquet with (
format ='PARQUET',partitioned_by=ARRAY['year]) as 
select *,year(order_Date) as year from sales_raw;
```

athena cost depends on scan data not number of rows,query time and so 🤑

partiiton pruning fail :
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
it doesn register partitions

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
