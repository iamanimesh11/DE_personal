# REDSHIFT-ANALYTICS WAREHOUSE

> Redshift=Distributed SQL engine over columar data,optimized for analytics(OLAP)
❌Not for single row lookups,freqeent updats
✅for aggregation,joins,scans,analytics

> 👉Redshift is AWS'answer to snowflake/Bigquery/Teradata

```
Send SQL
  ⬇️
leader node parses and plans query
  ⬇️
compute node process data in parallel
  ⬇️
columnar storage ->only needed columns scanned
  ⬇️
aggregated result returned
```

## Columnar storage

using row storage is slow for analytics but columnar storage wins-fast access

as:
* queries usially needed few columns,so scan only these
* massive compression
* less I/O faster queries -> lower cost

## Whats Node,slices

Node -> separate computer server -own cpu,own memory,own local storage
* each node can store data and execute sql operations indepednetly and in parallel

Redshift cluster -> group of nodes contains:
* one leader node
  * accept sql queries from clients
  * create query executuion plan
  * decide what compute node does what
  * aggregates results and return them to the user

* one or more compute nodes
  * store actual table data
  * perform scan,join,aggregration,fltering ,etc
  * works in parallel on different portion of data

❓ whats slice ? -> virtual processing unit inside a compute node

each slde get portion of node cpu,memory,data

its basically  a logical worker inside a machine

👉one node contain multiple slices

> data is distributed across slices not nodes,because:
  * distribution key matter
 * skew happens when some slice get more data than others
* one overload slice can slow the whole query


---
## how leader node parses and plan the query

* validate the query -> check sql syntax,object names,column and data type,permissions  calls as `parsing`
* query execution plan ->decies which table need to be scanned,compute node and slices do the work,how join should be performed,in what operation should happen
* each slide do its work ,apply logic and sent back the results. leader node merge results




## distributed styles 

Redshift is distributed -> data must be placed on nodes inteliigently.so wrong choice leads to data shuffling=slow queries


###  EVEN (DEFAULT)

* Rows distributed randomly
* balanced storage 
* ❌poor joins

✅so better is when no frequent joins ,small/staging tables

### KEY (most reliable)

* rows with same keys go to same node
* join become local (Fast)

✅better to use when large fact table,frequently joined on a column and ❌bad if key is skewed

meaning:

if one key value appears too often,example : country =`india` appears in 60% rows makes one node get overload and othe rnodes idle 

> high cardianlity,even distributed columns =good distkey
> low-cardianlity column =Bad DISTKEY

### ALL
-> full table copied to every node,

✅better to use when small dimension table,avoid join shufflinh ❌not for large table( Ilncreases cost)

---

## Sort keys (data skipping )

* defines physical order of data on disk. > store rows in this table in spcific order.

❓ why order matters ? -> as store data in blocks and read data blcok-by-block not row-by -row


> DISTKEY= node placement
> SORTKEY = row order inside a node

REDSHIFT store data in blocks and read data block by block ,not row by row means doesn't scan every row and check onditions one by one instead data splits into blocks.
each block has min and max values which helps tp distinguish the blocks called as `block pruning`

### Compund sort key

rows are sorted left -to-right ,column by column. basicALLY means first sort by first column and in case of same then applyies second column name as region

* best when queries with filter on first column
* mostly uses with time based queries

it fails on query like `where customerid =101` as order_Date not used and no pruning benefit

```
example: SORTKEY(order_Date,region)
```

### Interleaved sort key

* equal importance to all columns
* multiple filter patterns

baiscally rows beung arranged using a grid not a straight line. no single column dominate

Ex. 
```
Order_Date |region
-----------|------
25-01-01   | IN
25-01-02   | US
25-01-01   | US
2025-01-02 | IN

In compound it's easy to use and efficient but query where region= 'US' bad ,has to scan many blocks

So interleaved  make refshift store data so that :
  -  rows with same date cluster
  -  rows with same region also cluster

basically partal ordering for both ,not perfect ordering


Mmeory hack-if can't predict which column users will filter on then to use INTERLEAVED
```

---


# copy command

redshift is distributed system ,so how to load datra efficiently

`Insert INTO sales Values(...);` is just single-threaded,no parallelism as one node does most work

SO NOT designe dfor row-by-row inserts.

> **COPY** =parallel bulk load into Redshift from S3

so copy command read data from s3 and split files into chunks and each node load data in parallel,applie disturbution style while loading.

S3 is mandatory ,supporrs high throughput parallel reads 

---

# Redshift Spectrum

Lots of data in huge and dont want to copy into redshift to save cost but still want SQL,Join with Redshift tables

**Athena** is serverless but cannot join with redshift tables.so athena works alone,redshift works alone

So,spectrum allows to query data directly in s3 using sql without loading it into redshift


⭐ Performance rule:

fast only when data is in parquet,partitioned in s3,query select few columns not all

❌ but why even needed that spectrum and redshift when have athena ,glue

real world case -two types of data:

1. Hot data (busienss critita;)
   last few days sales
   used by dashbaordsl finance ,ops team
   need fast joins and queries
>>> store in **amazon redshift**

2. cold/hisotrical data . 
   old data,rarely queired,huge(tb),mostly for audit ,trend,ML
>>> store in S3 (cheap storge)

❓ question:give me last 7 days sales(redshift) + same week last year(s3 historical data) in one query

athena only approach would fail as no real time join,dashbaor dcant wait,complex orchestration,slow decision business
and athena cannot join with redshift tables

