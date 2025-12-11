CSV TO PAQRUET USING ATHENA : 

CREATE TABLE sales_parquet
WITH (
    format = 'PARQUET',
    external_location = 's3://my-de-lake-animesh11/sales_parquet/year=2025/month=1/',
    parquet_compression = 'SNAPPY'
) AS
SELECT *
FROM sales_raw
WHERE year = 2025 AND month = 1


csv to parquet using glue job:


# ===== Import Libraries =====
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.job import Job
from pyspark.sql.functions import lit
from awsglue.dynamicframe import DynamicFrame

# ===== Parse Job Arguments =====
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# ===== Initialize Spark & Glue Contexts =====
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ===== 1️⃣ Read CSV from Glue Catalog =====
datasource0 = glueContext.create_dynamic_frame.from_catalog(
    database="sales_demo_db",    # Your Glue database
    table_name="sales_sales"      # Your CSV table in Glue
)

# ===== 2️⃣ (Optional) Add Partition Columns =====
# Convert DynamicFrame to Spark DataFrame
df = datasource0.toDF()

# Add 'year' and 'month' columns for partitioning
df = df.withColumn("year", lit("2025"))   # change as needed
df = df.withColumn("month", lit("01"))   # change as needed

# Convert back to DynamicFrame
dyf_final = DynamicFrame.fromDF(df, glueContext, "dyf_final")

# ===== 3️⃣ Write as Parquet with Partitions =====
glueContext.write_dynamic_frame.from_options(
    frame=dyf_final,
    connection_type="s3",
    connection_options={
        "path": "s3://my-de-lake-animesh11/sales_parquet/",  # Output S3 path
        "partitionKeys": ["year", "month"]                   # Create folder-based partitions
    },
    format="parquet"   # Convert CSV → Parquet
)

# ===== 4️⃣ Commit Job =====
job.commit()
