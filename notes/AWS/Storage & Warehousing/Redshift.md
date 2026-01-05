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


## Sort keys (data skipping )

* defines physical order of data on disk. > store rows in this table in spcific order.

❓ why order matters ? -> as store data in blocks and read data blcok-by-block not row-by -row



### Compund sort key

* best when queries with filter on first column
* time based queries

```
example: SORTKEY(order_Date,region)
```

### Interleaved sort key

* equal importance to all columns
* multiple filter patterns