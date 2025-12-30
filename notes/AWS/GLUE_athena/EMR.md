# AWS EMR(Elastic MapReduce)

EMR = Managed cluster for distributed big-data frameworks

Key idea:
- You get actual EC2 machines
- You control cluster lifecycle
- You run Spark / Hadoop / Hive / Presto / HBase
- AWS just manages installation, scaling, failures

EMR=infra+compute, not serverless

❓ why EMR exist ? 

GLUE vs EMR

| Aspect               | Glue        | EMR               |
| -------------------- | ----------- | ----------------- |
| Compute              | Serverless  | EC2-based cluster |
| Control              | Low         | High              |
| Cost model           | Pay per job | Pay per node-hour |
| Long-running jobs    | ❌           | ✅                 |
| Custom Spark configs | Limited     | Full              |
| Streaming / ML       | Limited     | Strong            |
| Debugging            | Abstracted  | Full logs, SSH    |

👉 Glue = convenience
👉 EMR = power + flexibility

---
# Architecture

EMR cluster has node types:

1️⃣ Master Node
- Controls cluster
- Runs YARN ResourceManager
- Coordinates Spark jobs
- If master dies → cluster dies

2️⃣ Core Nodes
- Run task
- Store data in HDFS
- Required if using HDFS

3️⃣ Task Nodes
- Run tasks only
- No HDFS storage
- Cheapest → best for scale-out

**Note : Task nodes can be added/removed without data loss.**

---

## 🧠 EMRFS — Why EMR Loves S3

By default, modern EMR does NOT depend on HDFS.

Instead it uses EMRFS:
- A special filesystem layer
- Allows Spark/Hadoop to read/write directly to S3

So:
```
    Spark → EMRFS → S3
```
This makes EMR behave like a data lake processor, not a storage system.

---

💰 Cost Optimization (High Exam Weight)

🔹 Spot Instances in EMR
- Use Spot for Core + Task nodes
- Keep Master on On-Demand
- Massive cost savings (60–90%)

🔹 Auto-termination
- Kill cluster after job finishes
- Prevents accidental billing

📌 Exam question pattern:

`“Long batch job, cost-sensitive, fault-tolerant” → EMR + Spot`


---

⚙️ Running Spark on EMR (Mental Flow)

You don’t need commands now, just flow:
1. Create EMR cluster
2. Install Spark
3. Submit Spark job
4. Spark reads from S3
5. Writes back to S3
6. Terminate cluster

This is batch-first thinking


## 🔥 When EMR Is the Right Choice

Choose EMR when:
- Very large datasets (TB–PB)
- Long-running Spark jobs
- Custom Spark tuning needed
- ML pipelines (Spark MLlib)
- Streaming with Kafka
- Need SSH-level debugging

Choose Glue when:
- Simple ETL
- Event-driven pipelines
- Fully serverless preferred
- Low ops overhead