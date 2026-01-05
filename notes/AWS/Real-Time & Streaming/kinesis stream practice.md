# Practice Example

✔️ Kinesis Data Stream created

> Name: demo-kinesis-stream

> Shards: 1

stream is like an empty Kafka topic.

- > Kinesis does NOT push data to consumers.
- >Consumers must explicitly ask: “From where should I start reading?”

# ⭐ Producer step

```
aws kinesis put-record ^
  --stream-name demo-kinesis-stream ^
  --partition-key user1 ^
  --data "{\"user_id\": \"user1\", \"event\": \"login\"}"
```
Must pass base64 encoded data.
```python
encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
```

### EXPECTED OUTPUT 
```json
{
  "ShardId": "shardId-000000000000",
  "SequenceNumber": "49650000000000000000000000000000"
}
```

* ShardId → which shard your data landed in
* SequenceNumber → offset inside the shard -> This number is what ordering is based on

👉 This is Kafka offset in AWS language.


# ⭐ Consumer step - Read data from kinesis

**Step 1: GET the shard ID**

Run:
```json
aws kinesis describe-stream --stream-name demo-kinesis-stream
```
```json 
"Shards": [
  {
    "ShardId": "shardId-000000000000"
  }
]
```

**Step 2: GET a shard Iterator**

>“From where do I want to start reading?”

We’ll use: 
👉 TRIM_HORIZON = read from the oldest available record

```
aws kinesis get-shard-iterator \
  --stream-name demo-kinesis-stream \
  --shard-id shardId-000000000000 \
  --shard-iterator-type TRIM_HORIZON
```
Expected output:
```json
{
  "ShardIterator": "AAAAAAAAAA..."
}
```
📌 This iterator is like:

* Kafka consumer offset
* A pointer into the stream

🧠 Very important (exam + real world)

* Iterator expires in 5 minutes
* It is stateful
* After reading, must use NextShardIterator


**STEP 3: Fetch the record**
```
aws kinesis get-records \
  --shard-iterator AAAAAAAAAA
```
Output:
```
{
  "Records": [
    {
      "Data": "eyJ1c2VyX2lkIjogInVzZXIxIiwgImV2ZW50IjogImxvZ2luIn0=",
      "SequenceNumber": "4965...",
      "ApproximateArrivalTimestamp": 169...
    }
  ],
  "NextShardIterator": "BBBBBBBBB..."
}

```
🧠 Decode what you’re seeing (do NOT rush)

1️⃣ Data
* Base64 encoded
* That’s JSON (user1 login)

2️⃣ SequenceNumber
* Same offset you saw during put-record
* Ordering guarantee anchor

3️⃣ NextShardIterator
* Where the consumer continues next
* This is how streaming consumption works

```
Shard
 ├── Record 1 (seq 100)
 ├── Record 2 (seq 101)
 └── Record 3 (seq 102)
         ↑
     iterator moves forward
```

## all above is just simple approach work at low level ,not in Production.- raw Kinesis API usage.


# 🔹 What happens in production

## Option 1: Custom app (SDK)

Your app:
* Uses AWS SDK (Java, Python, etc.)
* Calls GetShardIterator
* Calls GetRecords in a loop
* Stores last SequenceNumber (DynamoDB, Redis, DB)

🧠 You = the consumer framework


## Option 2: KCL (Kinesis Client Library)

AWS-managed consumer framework

It:
* Manages shard leasing
* Handles resharding
* Tracks checkpoints
* Uses AFTER_SEQUENCE_NUMBER

🧠Still calls the same APIs under the hood


## Option 3: AWS Lambda consumer

You:Attach Lambda to the stream
AWS:
* Polls shards
* Manages iterators
* Handles retries
* Scales automatically

🧠 You never see iterators — but they still exist

## Option 4: Enhanced Fan-Out (EFO)

You:
* Register a consumer
* Subscribe to a shard

AWS:
* Pushes records to you
* Gives you a dedicated iterator
* Tracks state internally

Still Sequence numbers,Ordering,Cursor logic

```
AWS serves:
Startups → Lambda
Enterprises → KCL
Specialized systems → Custom apps
High-scale analytics → EFO
```

### 🏆 Exam-style summary table (memorize)

| Option     | Why it exists        | Best for                |
| ---------- | -------------------- | ----------------------- |
| Custom App | Full control         | Specialized logic       |
| KCL        | Production consumers | Long-running apps       |
| Lambda     | Zero ops             | Event-driven            |
| EFO        | Isolated performance | Multiple fast consumers |


## Lambda as consumer

> Lambda polls via Event Source Mapping (hidden GetRecords loop)

Internally:
* Lambda keeps pulling records
* But the checkpoint stored by the Event Source Mapping:
   * advances only after success
    * is what defines replay position


**Lambda batch = shard-scoped, not stream-wide**

A single Lambda invocation:
* never mixes shards,always processes one shard at a time

> Parallelism = number of active shards

So your timeline is:
```
Shard-0001 → Lambda invocation A
Shard-0002 → Lambda invocation B
```

Failures are isolated per shard - not global.

**Partial batch response changes who retries what**

Old behavior: Any failure → retry entire batch

New behavior (Partial Batch Response)

You return:
```json
{
  "batchItemFailures": [
    { "itemIdentifier": "sequenceNumber-123" }
  ]
}

AWS then:
Advances checkpoint past successful records
Retries only failed ones
```

## 🎥 KCL SIMULATION - REAL TIME, REAL FAILURES

Pipeline
```
Producers → Kinesis Data Stream → KCL Workers → S3
```
Components

* Amazon Kinesis Data Streams
* Kinesis Client Library (KCL)
* Amazon DynamoDB (VERY important)
* Amazon S3

KCL runs on: EC2,ECS,EKS,On-prem (doesn’t matter)

>KCL does NOT store checkpoints in Kinesis
store everthing in  **DynamoDB** 

* Shard ownership (leases),
* checkpoints (sequence numbers),
* Worker coordination

📌 This is why KCL scales horizontally without Lambda magic.

🗂️ DynamoDB tables (created automatically)
| Table         | Purpose                        |
| ------------- | ------------------------------ |
| `LeaseTable`  | Who owns which shard           |
| `Checkpoint`  | Last processed sequence number |
| `WorkerState` | Heartbeats & liveness          |


🕒 T0 — Stream exists

Kinesis stream has:
```
Shard-0001
Shard-0002
```

🕒 T1 — Workers start

You launch 2 KCL workers:
* Worker-A ,  Worker-B

Each worker:
* Registers itself
* Reads LeaseTable
* Tries to acquire shard leases

🕒 T2 — Lease assignment

DynamoDB now looks like:

| Shard      | Lease Owner |
| ---------- | ----------- |
| Shard-0001 | Worker-A    |
| Shard-0002 | Worker-B    |

🧠 Only the lease owner may read a shard

This is how KCL guarantees:No double consumption,Ordered processing per shard

🕒 T3 — Polling begins

Each worker independently:
```
GetShardIterator
GetRecords
ProcessRecords
```

🕒 T4 — SUCCESS PATH

Worker-A processes batch successfully.

What happens:
* Writes to S3 ✅
* Calls checkpoint(sequenceNumber)
* Updates DynamoDB
* DynamoDB checkpoint now: Shard-0001 → seq-999

🎉 Shard advanced

### 💥 FAILURE SCENARIOS (THIS IS THE GOLD)

#### 💥 FAILURE 1 — Worker crashes mid-batch

Worker-A dies after:

login ✅ page_view ✅ logout ❌

What does NOT happen

❌ No checkpoint written,❌ DynamoDB unchanged

What DOES happen:

Lease heartbeat stops, Lease expires (default ~10s)

🧠 From KCL’s perspective, NOTHING was processed


🔁 T5 — Rebalance occurs

Worker-B notices:
Lease expired for Shard-0001

Worker-B steals the lease.

DynamoDB:
| Shard      | Lease Owner |
| ---------- | ----------- |
| Shard-0001 | Worker-B    |
| Shard-0002 | Worker-B    |


Worker-B now:Starts reading from last checkpoint,Reprocesses entire batch

⚠️ Duplicates happen

✔️ At-least-once delivery


#### 💥 FAILURE 2 — Poison pill record

One record always crashes your code.

Worker retries and Checkpoint never advances and Shard becomes stuck

🧠 This is why KCL apps must:

Catch per-record exceptions and  Skip / DLQ / quarantine bad events

----

### Resharding happens:

it happens when shard overflow to its limit and then new shard are created but new shards can only be read when parent shard marked as 
checkpoint ended

---

## CASE When Lambda fails and KCL needed

⭐ Lambda  Time limit :⏱️ 15 minutes max execution

So problem when `training a model` ,`Running heavy aggregation`,` Replaying hours of historical data`,`Doing large windowed joins` requies

⭐ With KCL  can:
* Control checkpoint timing
* Commit after downstream transactional success
* Align checkpoints with DB transactions

but lambda can't ❌

⭐Stateful stream processing

means when program need to remember whats previous data was like in forecasting .

Remember earlier events,That memory is called state.

1️⃣ Session windows means `Group events that happen close together.`

2️⃣ Rolling aggregates means ` numbers that keep updating` ex Number of clicks in last 1 hour

4️⃣ Fraud detection over time :`system must remember past behavior`

**SO Lambda runs does the job and forget everything then dies**

It's stateless by design

**Since Lambda forgets: You must store memory in DynamoDB or Redis**

Sometimes Lambda:Starts from zero,Takes time to wake up

For real-time processing, this is bad 🚨

---
> ## KCL = Kinesis Client Library is like A program that keeps running instead of restarting

---

⭐ Massive fan-in, limited fan-out

Lambda scaling = number of shards.

If:
* 1 shard
* 1000 TPS
* Heavy CPU logic

❌ Lambda:
One invocation at a time
Bottlenecked

✅ KCL:
Multiple threads
Async processing
Internal parallelism (within shard order constraints)

---

# where does EPO(ENHANCED FAN OUT ) places in architecture

EPO is for consumers ,like 1 shard in stream where data is being written 

Enhanced Fan-Out gives each consumer its own private read pipe.

```
Shard-0001
   ├── Consumer A → 2 MB/sec
   ├── Consumer B → 2 MB/sec
   └── Consumer C → 2 MB/sec
```
```
Producers
   ↓
Kinesis Data Stream (shards)
   ↓
Enhanced Fan-Out (optional)
   ↓
Consumers (KCL / Lambda / Flink)
```

⭐⭐ Benefits:

* Low latency (~70 ms)
* No polling
* Dedicated throughput
* Independent consumers