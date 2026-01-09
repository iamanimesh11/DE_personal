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


# EXAMPLE CASE

> Store user orders for an e-commerce app

for que like :
* get all order of a user
* get orders in time range
* get latest order
* handle million of users

CREATE A TABLE -> PK=user_id, SK=order_timestamp(str/num)

primary key =(user_id,order_timestamp)

#### so,DynamoDB store all item with same PK on same parttion ,sk keep them sorted inside that partition

bad as million of user -> same pk, all traffic in one partition

> lARGE RATE vol is fine but high req rate on one PK is dangerous ⚡

## Reading data :

1. GetItem - fastest ,but limited:
   * means give me one exact item must be provided full primary key
   * dynamodb hash pk ->find partition,binary search sk -> fetch item 
2. Query -give multiple item with one partiiton
  mandatory - partition key =exact match,optional =sort key

filterepression apply after data is read ,so cost remain same

3. scan - slow and expensive
   reads all parititon,check every item and consume massive RCUs


## DynamoDB index

not like in relational database but **alternate table* with a differrent primary key,baiscallh different  data struc

brain hack:-> index =/ pointer but another table automaicallt maintained by AWS

* index have own pk/sk and capacity
* costs money

  Its needed becquae ,can't efificiently do :

  ```
  amount >500
  status ='Delivered'
  product_id='P123'
  ```

  becuase it understand ony PK/SK ,others is scan (bad)

  🔥indexes exist to add new access patterns

  Types  : LSI (local secondary index) ,GSI (global seocndary index)
  
### LSI 

basically same PK but different SK , 

in case when query is for another attribute that is not present - can be used 

like in case 'get all orders of user sorted by **order_amount** instead of time 

💫LSI must be created at TABLE CREATION TIME, can't add 

LSI share RCU.WCU  wuth base table.

#### why don't multiple sort keys 

❌doesn't allow becuase it physiclally stores the data in only one sorted order per partition

dynamodb avoid pointer which uses in rdbms for speed and scale

### GSI -GLOBAL SECONDARY INDEX

-> Has OWN PARTITION KEY AND SORT KEY

example case : get all order where status ="delivered" ,so across all users.

base table is impossible .
LSI is impossile (same pk)

features:
 * can be created ,deleted,anytime
 * supports new access patterns

so, new query requirement afte production -choose **GSI**


⭐ So ,LSI reorganize data inside the same partition .GSI created a new way to access data across partitions

**WHAT DOES CONSISTENCY MEANS**

consistency here means when data is being read does latest write immedialty appears or not?

Strong : immediately,no delay
* strong reads consume double RCUs
  
evenutal: after short delay ,read return data - defauly in dynamodb

Physical Placement:
 LSI:Local Secondary Index
 * lives in same partition,same node physical ,same write path,, so **Strong consistency is possible**

GSI: live in different partition,diff node,separate scaling  so there is replication lag


## Whats RCUs and WCUs ?

WCU (write capacity unit) -> 1 wcu = 1 kb write per second
>basically writes are rounded up

RCU (read capacity unit) ->
* strong consistent read = 1RCU = 4kb/s
* evenutal consistent read = 1 rcu = 8kb/s
* so eventual read are cheaper ,stronger reads cost 2x so expensive

## Index impact on capacity 

base table +index =multiple writes
so  if 1 tabke and 2 gsi then  1 write will includes 3 writes so write cost multiplied

💫Reads:
 * reading from GSI uses GSI RCUs
 * reading from LSI uses table RCUs

## capacity modes: 

### provisioned capacity -specify RCUs,WCUs  -> when trafic is predictable
### on demand capacity 


## throttling:
when request > provisioned RCUs/WCUs makes bust exceed limits
symptoms : `provisionedthroughputexceededexception` ,so better is to beter pk design ,use on demand or add write sharding

# scaling ,hot,partition and design patterns

dynamodb auto create more partition only when PKs are well distributed as it has fixed storage limit 

solution of hot partition is to make randomness basically add sharding

GSI index can become hot partition as well like key Status as Active


##  dynamoDB  streams

basically to do sth when data changes in dynamoDB

DynamoDB streams change data capture (CDC) ,it :
* record every change to items
* near real time
* ordered per partition
* Strean capture :INSERT,MODIFY,REMOVE

  basically it works like:
  ```
  write happens -> changes written to stream -> consumer reads stream -> action performed
  ```

⚡so consumer mostly is `lambda`

ech record contains: event type,timestamp,item data (depends on config)

Stream view types :
* keys_only -pk and sk
* new_image -item after change
* old_image - item before change
* new_and_old_image - before+after (for comparison)


> orderingis possible within a partition key and at least once delivery ,not global ordering
> stream=/ long term audit kinda,only for 24 hours -retention limit
> streams aren't enabled by default

