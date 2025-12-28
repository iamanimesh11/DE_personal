# 🟧 Processing Layer 

## AWS Glue ETL -> pyspark on AWS
Serverless Spark platform for large-scale data transformation

GLUE JOB TYPES :
1. Spark Job Types
2. python shell jobs -small task like  metadata ops,API calls
3. Ray jobs -parallel python workload

In normal Spark (EMR / local Spark): only  DataFrames
In AWS Glue:AWS introduced DynamicFrames (to solve schema & semi-structured data problems in data lakes)

✅ DynamicFrames vs DataFrames
| DynamicFrame       | DataFrame         |
| ------------------ | ----------------- |
| Glue-native        | Spark-native      |
| Schema flexible    | Schema strict     |
| Handles dirty data | Fails on mismatch |
| Slower             | Faster            |

```
S3 → DynamicFrame → (optional) DataFrame → write
```
Dyamicframe is schema flexible and it handle issue like :
json file with missing field,csv where column order changes,nested strcutres so and so. 
Spark fails but dynamicframe handles on its own.

**Dataframe** is still needed as its:
faster,richer api,full spark sql support,industry standard

so dyamicframe used to ingest data and then conver to DF to transform.

🔥 minimal working example:
Read from Catalog(glue native) :
```python
dyf = glueContext.create_dynamic_frame.from_catalog(
    database="sales_demo_db",
    table_name="sales_sales"
)
```
convert to dataframe:
df=dyf.toDF()
#spark things(join,filters,agg)
df_filtered = df.filter(df.sales > 5000)
convert back:
dyf_out = DynamicFrame.fromDF(df_filtered, glueContext, "dyf_out")

**Rule to remember**:
🔁 Read with DynamicFrame → Convert → Transform with DataFrame → Write back

✅ Job Bookmarking (Incremental Loads)
Glue remembers what data it already processed-so avoid reprocessing old files.
Glue bookmarking works based on:
✔ File paths (S3 objects)
✔ Timestamps
✔ Job run ID
✔ Source type (S3 / JDBC)
**Bookmarking works BEST with append-only data.**

Bookmarking and partitioning both are different one is for processing and one is for query 
If question says:Incremental ETL,Avoid reprocessing,Append-only S3 data,Serverless
👉 Answer involves Glue Job Bookmarking

📌 Common exam trap:
Bookmarking is job-level, not table-level.

Bookmarking + Dynamicframe
bookmarking only works reading via glue abstraction like
```
glueContext.create_dynamic_frame.from_catalog(...)
```
```
from_options(connection_type="s3", ...)
```
❌ If you use plain Spark spark.read.csv() → bookmarking is bypassed.

❓ Question:
Glue job with bookmarking enabled still reprocesses data. Why?

✔ Possible answers:
Files overwritten instead of appended,Spark DataFrame API used instead of DynamicFrame,Bookmark reset , Same S3 path reused

🔁 Reset Bookmark (Controlled Re-run)
```
--job-bookmark-option job-bookmark-reset
```
used for backfill requried,schema changed,logic updated

✅ Glue Workflows-airflow lite
can run crawlers,jobs,handle dependencies

🧠 Glue vs Lambda vs EMR (EXAM GOLD)

| Use Case                                               | Choose |
|--------------------------------------------------------|--------|
| < 15 min, event-driven, small/stateless workloads      | Lambda |
| Batch ETL, serverless, managed Spark                   | Glue   |
| Big data at scale, heavy Spark tuning, custom libs     | EMR    |


🟧 Glue Job Troubleshooting (Exam + Real-World Focus)

Glue ETL job = Managed Spark job running on AWS INFRA
❌ Job fails immediately:
Causes:
   IAM role missing permissions
   S3 path typo
   Wrong script location

**"Job failed during initialization"**
check IAM role has s3:GetObject,s3:PutObject,logs:*

❌ Crawler works, Athena works, Glue job fails.
causes: schema mismatch,csv header issue,wrong delimiter
example: Glue inferred id as string,Spark expects bigint
1. Glue crawler scan file and guesses column type so if it has mixed value it defualt to string.so craeler say   `id=string`
2. athena can auto cast string to number when querying ,so still works:
   `SELECT CAST(id AS BIGINT) FROM table;`
3. glue spark job is strict  ,it still expect same type /

correct fix:explicitly control the schema

option1 : applymapping()
`mapped_df = ApplyMapping.apply(
    frame=source_df,
    mappings=[
        ("id", "string", "id", "long"),
        ("name", "string", "name", "string")
    ]
)
`
foces glue to treat id as bigint

✖️🔴OutOfMemory / Executor Failures
Job runs → fails mid-way,
Error mentions executor lost / GC overhead

causes: too large files,many partitions,wrong worker type
✅ Fix:
- Increase worker type (G.1X → G.2X)
- Reduce shuffle
- Repartition wisely
Glue job memory issues → scale workers, not retries



