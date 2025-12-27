# 🟧 Processing Layer 

## AWS Glue ETL -> pyspark on AWS
Serverless Spark platform for large-scale data transformation

GLUE JOB TYPES :
1. Spark Job Types
2. python shell jobs -small task like  metadata ops,API calls
3. Ray jobs -parallel python workload

✅ DynamicFrames vs DataFrames
| DynamicFrame       | DataFrame         |
| ------------------ | ----------------- |
| Glue-native        | Spark-native      |
| Schema flexible    | Schema strict     |
| Handles dirty data | Fails on mismatch |
| Slower             | Faster            |
