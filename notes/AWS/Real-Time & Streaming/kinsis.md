🟥 PHASE 4: Real-Time & Streaming
6️⃣ Amazon Kinesis Data Streams
Deep Master:
- Shards, retention, enhanced fan-out
- Consumers: Lambda / KCL
- Scaling

Exam Focus:

- Provisioned vs On-demand shards
- Ordering guarantees

7️⃣ Amazon Kinesis Firehose

Deep Master:
- Delivery to S3, Redshift, OpenSearch
- Transformations (Lambda)

Exam Focus:

- S3 prefixing
- Buffer interval vs data freshness

8️⃣ Kinesis Data Analytics

- SQL queries on streams
- Sliding windows, tumbling windows(Only deep where exam needs.)

---

Mental shift first:

    Until now → data already in S3
    Now → data is continuously arriving (events)



# AMZON KINESIS DATA STREAMS(KDS)

Purpose: capture & store real time streaming data like log events,IOT data for processing.

⭐ Features:
- data is stored in shards,each shard can handle fixed number  of read/write per second
- data retention:default 24 hrs,can extend to 7 days
- Supports multiple consumers reading from the same stream.
- You need to write your own applications (using AWS SDK, KCL, or Lambda) to process the data.


⭐ use case exmple:
- real time fraud detection in banking transaction
- Processing IoT device telemetry data.

⭐ Analogy:

- Think of it as a conveyor belt where raw data items come in, and you decide who picks them up and what to do.


# AMZON KINESIS DATA FIREHOSE

⭐ Purpose:
- Fully managed service to deliver streaming data directly to    destinations like S3, Redshift, Elasticsearch, or Splunk.
- No need to write consumers; it automates the ingestion, transformation, and delivery.

⭐ Key Features:

- Can transform data using AWS Lambda before delivery.
- Supports near real-time delivery (buffered based on size or time).
- Fully managed, so no shard management or scaling worries.

⭐ Use Case Example:

- Storing web server logs to S3 for analytics.
- Streaming clickstream data to Redshift for reporting dashboards.

⭐ Analogy:

Think of it as a pipeline that takes your incoming data and drops it automatically into a warehouse or storage, optionally shaping it along the way




3. Kinesis Data Analytics

⭐ Purpose:

- Analyze streaming data in real-time using SQL or Java/Scala.
-Works on top of Kinesis Data Streams or Firehose.

⭐ Key Features:

- Real-time analytics without setting up your own processing cluster.
- Can run continuous queries on streaming data.
- Can output results to Kinesis Firehose, Streams, or Lambda.

⭐ Use Case Example:

- Real-time metrics on IoT sensor data.
- Counting events per minute in streaming logs.

⭐ Analogy:

Think of it as a live dashboard that constantly calculates stats on your incoming data.


# Quick Comparison Table

| Feature / Service  | Kinesis Data Streams          | Kinesis Data Firehose                   | Kinesis Data Analytics               |
| ------------------ | ----------------------------- | --------------------------------------- | ------------------------------------ |
| Type               | Stream storage & ingestion    | Delivery pipeline                       | Real-time processing/analytics       |
| Managed            | Partially (you manage shards) | Fully managed                           | Fully managed                        |
| Data Retention     | 24h (extendable to 7d)        | N/A (delivers data immediately)         | Depends on source (Streams/Firehose) |
| Transformation     | Manual via consumer app       | Lambda-based transformations            | SQL/Java/Scala queries               |
| Output/Destination | Custom apps/Lambda            | S3, Redshift, Elasticsearch, Splunk     | Streams, Firehose, Lambda            |
| Typical Use Case   | Custom real-time processing   | Automatic delivery to storage/warehouse | Real-time analytics and metrics      |














---


🏗️ CORE MENTAL MODEL (This is the heart)
Imagine this physically:

- A stream is a road
- The road has lanes → those are shards
- Cars (events) move forward only
- Inside one lane, cars are strictly ordered
- Between lanes → no ordering promise

That’s it. That’s Kinesis.

## 🧱 What is a Shard really?

Not jsut a storage,but 3 thing at once:

### 1️⃣ Ordering boundary- throughput limit
- scaling unit 

inside each shard,events are writtent/read in same order.

Across MULTIPLE shards 
```
Shard 1: Order-1 → Order-3
Shard 2: Order-2 → Order-4
```

AWS says:
- “I don’t promise anything”
Meaning:
- Order-2 might be processed before Order-1
- Cross-shard ordering is undefined

👉 Ordering only exists INSIDE a shard


### 2️⃣ Throughput limit

👉 How much data can flow per second?
| Direction | Limit per shard               |
| --------- | ----------------------------- |
| Write     | 1,000 records/sec OR 1 MB/sec |
| Read      | 2 MB/sec                      |

If you exceed it:
❌ Throttling happens
❌ AWS rejects extra writes

👉 Shard = speed limit

### 3️⃣ Scaling unit
- Not scale CPU or memory
- scale shards

Example:
```
Traffic = 800 records/sec → 1 shard OK
Traffic = 3,000 records/sec → need 3 shards
```
Scaling methods:
- Split shard (scale up)
- Merge shards (scale down)

👉 Shard = unit of scaling

## 🔑 What is a Partition Key REALLY?
When you send one record (event) to Kinesis, AWS forces you to answer one question:

❓ “Which shard should this record go to?”

You don’t choose the shard directly.

Instead, you provide:
` partition_key = "some value" `

AWS do:
- hashes the partition key
- hash result map to ONE shard
- record goes into that shard

🔥 The Golden Rule (never forget this)
- Same partition key → same shard → order guaranteed

**AWS wants:**
- Parallelism (multiple shards)
- Ordering where needed

Partition key lets YOU decide:
- What must be ordered together
- What can be parallel

## 🔥 What is a Hot Shard (1-line)
A hot shard happens when too many records go to the same shard, exceeding its throughput limit.

Root cause:
👉 Bad partition key choice

`Same partition key → same shard`

So hot shards happen when:
- One key appears far more often than others
- OR you use a constant / low-cardinality key

🧠 Goal when designing partition keys

You must balance 3 things:
- Ordering (what must stay in order)
- Distribution (spread load)
- Throughput (avoid 1 shard overload)

✅ Proven techniques to avoid hot shards

### 🟢 1. Key bucketing (MOST IMPORTANT)

❌ Bad example:partition_key = user_id

✅partition_key = user_id + "#" + (hash(user_id) % N)
```
user_42#0
user_42#1
user_42#2
```
this Spreads one user across N shards

🟢 2. Composite keys (smart distribution)

❌ Bad example:` partition_key = country`

✅partition_key = country + ":" + user_id

Result:
- Keeps regional grouping
- Avoids all traffic from IN hitting one shard

🟢 3. Time-windowed keys (streaming analytics)

❌ partition_key = sensor_id

✅ partition_key = `sensor_id + ":" + yyyyMMddHH `

```
sensor_12:20251230-10
sensor_12:20251230-11
```

Result:
- ordering preserved per hour
- Load spreads over time


🟢 4. Detect hot shards early (production rule)

Monitor CloudWatch:
```
IncomingRecords
IncomingBytes
WriteProvisionedThroughputExceeded
```
If one shard spikes, your key design is wrong.

---

## 📦 What ACTUALLY flows in Kinesis?
A record is the smallest unit of data in Kinesis.

DATA PAYLOAD:
```json
{
  "order_id": "A123",
  "user_id": 42,
  "amount": 999,
  "timestamp": "2025-12-30T10:00:01Z"
}
```
- Partition Key (routing decision) decides:
Which shard does this record go to?

📌 Same key → same shard → ordering preserved.

- Sequence Number (ordering + position)- assigned by AWS
means `“Which record came before or after this one?”`

in shard `Shard 1:
(seq=1001) → (1002) → (1003) → (1004)
`

When a producer sends data:

Kinesis stores
```json
{
  "data": "...",
  "partition_key": "user_42",
  "sequence_number": "496392847...",
  "shard_id": "shard-0001"
}
```
Consumers then:
- Read records in order
- Track last processed sequence number
- Resume safely after failures

## 🔄 How Kinesis consumption actually works

1. Consumer reads record with sequence_number = 100
2. Consumer processes the data (DB write, API call, etc.)
3. Consumer checkpoints:
👉 “I’m done up to sequence 100”
    -  Checkpointing = telling Kinesis
    - “You can consider these records processed”

###  💥 Where things go wrong (and duplicates are born)

**Case 1: Crash AFTER processing, BEFORE checkpoint**
```
Read record 100
✔ Process record (DB write done)
💥 App crashes
❌ No checkpoint saved
```
when consumer restarts
```
Reads record 100 again
```
➡️ Duplicate processing happens

**Case 2: Network / timeout issue**
```
Read batch of records
Process them
Checkpoint call times out
```
To be safe:
➡️ It retries → duplicates

**Case 3: Lambda-based consumers (very common)**

With Kinesis + Lambda:
- AWS retries batches automatically on failure
- If Lambda fails midway:

Entire batch is retried

Records already processed → processed again

Again:
➡️ duplicates

---

**Note: Scaling compute without scaling shards does nothing**
**Note:🧠 Parallelism = Number of Shards**

🧠 Consumer Types 

1️⃣ Shared throughput (classic pulling)
- Consumers share shard read limits
- Can get throttled

2️⃣ Dedicated throughput
- Each consumer gets its own pipe
- No interference

##  ⁉️ What happens if multiple consumers read the same shard?


### ⭐ Shared Throughput Model (The Default, Oldest One)

One shard = one pipe

All consumers drink from the same pipe

So:
- If one consumer is slow → others suffer
- If many consumers read → throttling happens
 
Why AWS allowed this, Because:

`Simple,Cheap,Works fine for 1–2 consumers`

This is the classic pull model, similar to early Kafka consumers.

🔴 Key Intuition (Lock this in)

**Throughput is shared per shard, not per consumer**

So:
Shard = 2 MB/s read
```
2 consumers → each gets ~1 MB/s
4 consumers → worse
```

### ⚠️ The Pain Point (Why This Model Breaks)

Imagine:

- Fraud detection service
- Real-time dashboard
- Logging pipeline

All reading the same stream.

Suddenly Lag increases,Throttling errors,Ordering delays

AWS needed a solution without breaking ordering.

### ✅ Enhanced Fan-Out (EFO) - Why it Exists

**Enhanced Fan-Out gives each consumer its own private pipe from the shard.**

Instead of:
```
Shard → One Pipe → Many Consumers
```

> You get:
```
Shard → Pipe A → Consumer A
     → Pipe B → Consumer B
     → Pipe C → Consumer C
```
Ordering is still preserved
Throughput is no longer shared

❓**What Changed Conceptually?**

Nothing about:`Shards`,`Partition keys`,`Ordering`,`Retention`

Only how data is delivered to consumers.

**Enhanced Fan-Out does NOT:**
- Increase write throughput
- Change shard limits
- Change partitioning

It only fixes Consumer-side contention

❓**🧠Why Not Make EFO Default?**

Because:
- It costs more (EFO is billed per consumer per shard)
- Many use cases don’t need it
- One consumer is most common
  - Common patterns:
     - One Lambda
     - One analytics pipeline
     - One ETL job

AWS gives choice, not force.

## ❓Why AWS Cannot Auto-Scale Shards Invisibly ?
If AWS auto-added shards silently:
- Partition key → shard mapping would change
- Ordering could break
- Consumers could miss data

 So AWS says:

“You decide when ordering boundaries change.”

That’s why:

Shard scaling is explicit

**Scaling Shards = Changing Parallelism**

So AWS introduced:

- Provisioned mode → You manage shards
- On-Demand mode → AWS manages shard scaling internally

---


