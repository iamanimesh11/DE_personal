# What problem dynamoDB solves?

S3+REDSHIFT are good for:

> analytics,reporting,dashbaord,aggregration,historical analysis
so basically OLAP model.

Basically are **thinking systems**

⚠️ PROBLEM TYPE: “RIGHT NOW” decisions

Questions like:

* “Is this user allowed to log in?”
* “Has this order already been processed?”
* “What is the current status of this payment?”
* “Rate-limit this API call”
* “Check inventory before confirming order”

they need single digit millisecond latency,million of request per second,no scanning,no waiting

when run normaly query like
```sql
SELECT status
FROM orders
WHERE order_id = 'ORD123';
```
makes Cold start latency,Query planning overhead,Disk-based reads,
Concurrency limits


✅ ENTER DynamoDB (why it exists)

DynamoDB exists to answer ONE QUESTION extremely well:

> “Given a key, give me the value — NOW.”

That’s it.

No joins.No scans (ideally).No analytics.

#### so its like giant distributed hash table works on key,value

# Type sof transaction - level data

## Type A - operational. / Real-time

It basically means "whats happening right now" like question"
 like ex:
 * has this order alreayd been placd
 * whats current status
 * did payment succeed
 * can user clcik buy again

 key characteristics:
   * very fast(ms),read/write a lot/simple question to simple answer,
   * must scale massively

sotrage:
 * Redis,dynamodb,casssandara,,in memory cache kinda


## Type B -relational/financial/consitency heavy data

basically to answer **whats actually happened ,exactly>=?**

like order,payment ,inovices and reunds,audits,reports

 key characteristics:
* correctness over speed
* strong consitency(ACID)
* RELATIONSHIP BTW MANY TABLES

  storage:
  postgresql,mysql,oracle,sl server
  

# DYNAMODB VS RDS/AURORA  VS RESHIFT

## DynamoDB

NOSQL db for faster data fetch like user sesion,caches,deduplication,rate limi,inventory checks

## RDS/Aurora -transactional -sql db for AWS

sql db for strucutred data like orders,payments,invoices ,refunds, so and s

because -strong ACID gurantee,sql joins,contraitns,

## Reshift -analytics truth

used for daily sales,revenue report ,dashboard

## S3 -historical truth

for older data like raw logs,trasactions,audit history


# DYNAMO-DB Data Model

Not table = rows & columns  but collection of items and each item is identifed by primary key

```
no joins,foreign keys,relationship
```

Primary key types -> 

**simple primary key -ex. partition Key=user_id**

* determines where data is sotred
*  control scalability,performance

> decies which machine data goes to,aws hashes the pk -> assign it to partition

composite primary key - partition key(pk) +sort key

* order data inside same partition ,enables rane queries time based queries and sorting

⏰ exam trap: bad pk design
```
PK=country
```
bad as million of user -> same pk, all traffic in one partition
