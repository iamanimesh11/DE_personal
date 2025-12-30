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
from pyspark.sql.functions import input_file_name, regexp_extract
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
    database="sales_demo_db",      # Your Glue database
    table_name="sales_sales"       # Your CSV table
)

# ===== 2️⃣ Convert to DataFrame for transformations =====
df = datasource0.toDF()

# ===== 3️⃣ Extract year and month from S3 path =====
# input_file_name() gives full S3 path of each row
df = df.withColumn("full_path", input_file_name())

# Extract year and month using regex
df = df.withColumn("year", regexp_extract("full_path", r"year=([0-9]+)", 1))
df = df.withColumn("month", regexp_extract("full_path", r"month=([0-9]+)", 1))

# Drop helper column if needed
df = df.drop("full_path")

# ===== 4️⃣ Convert back to DynamicFrame =====
dyf_final = DynamicFrame.fromDF(df, glueContext, "dyf_final")

# ===== 5️⃣ Write as Parquet with partitions =====
glueContext.write_dynamic_frame.from_options(
    frame=dyf_final,
    connection_type="s3",
    connection_options={
        "path": "s3://my-de-lake-animesh11/sales_parquet/",  # Output S3 path
        "partitionKeys": ["year", "month"]                   # Automatic partitions
    },
    format="parquet"
)

# ===== 6️⃣ Commit Job =====
job.commit()
