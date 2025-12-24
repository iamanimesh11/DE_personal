# ⭐AWS Glue Data Catalog:

-> central metadata store(like library catelog) for all data stored across s3,redshift,and more
-> does not store the actual data ,only descriptive of data like metadata -the scehma ,location,format,partitons etc

heart 💙 of aws serverless analytics used by AWS GLUE,ATHENA,EMR ,REDSHIFT ,AWS LAKE FORMATION.

Ths centralized catalog makes sure :
  every service dont need schema definitions
  schema definition dont requrie manual update
  unified governance and access control.
this helpful in lake formation,
becuase of glue schema ,athena(sql query tool) can query s3 files instantly because it already know the schema.

Core components:
**Database**-logical contianer
**tables**-repesent metadata about a dataset ,doesnt contain actual data.
  key properties: s3 location (prefix),file format,column names + data types,partition keys ,SerDe(Serializer/deserializer)
**crawlers** : glue crawler which crawl or look at data (like s3 folder),detect schema ,create /update tables in data catalog.
    it automatically recognize partitions,nested json,file format,incremenal data addition
**classifiers** (used by crawlers):crawler understand the strucutre with the help of classfiier  ,
    types : json classifer ,csv,grok,xml,custom

**schema reigstry** :it store schema version for event based or kafka data .
    useful for : streaming pipelines,backward/forward capabilities,schema evolution


⭐ how glue fit into pipeline:
examole :S3 ->GLUE CRAWLER ->GLUE DATA CATALOG ->ATHENA ->GLUE ETL ->REDSHIFT SPECTRUM

athena query s3 like database,glue job use schema for transformation,
redshift spectrum can join s3 +redshift tables
govenerance via lake formation.

✴️ thats the foundation of aws data lake architecture

**Note: glue crawlers work better when data is inside folder ,not in bucket root**

## partitioning a data in S3
partitioning speed up queries ,reduces cost and make etl pipelines more efficient

Why❓ ,
Athena scan data fom s3 if have thousand of files ,then it will read everyhting .
partitioning let athena read only the folder needed.
exmaple: s3://bucket/sales/year=2025/month=01/day=01/sales.csv
now this shows it has logically partition of keys :year,month,day
so sql query like `select * from sales where year =2025 ;` will read that spcific folder only (2025)
**note: partition work for equal sign '='**

now crawler need to be modfied to detect partitions ,running crawler again will detect there is partiiton in s3 path.
so table already exist ->update it ,if new partition found -> add them 

when hit query `select * from sales;` will return same but when spcify foler name in where condition will reutrn output of data exsit in only the foler of that year


# ⭐ GLUE ETL JOB

anything which must run on any spceific schedule can be used in job.
glue jobs are based on workers (like how sspark folllow beneath the suface)

## covnert csv to parquet
s3 path : s3://bucket/sales/year=2025/month=01/day=01/sales.csv
glue etl job output must be:  s3://bucket/sales_parquet/year=2025/month=01/day=01/sales.parquet

athena will query this parquet fastter than csv 

new bucket path need to be created like `s3://bucket/sales_parquet`

new GLUE job:
    NAME -csv_toparquet
    soruce- sales_Demo_Db (database)
    table- sales_sles
    transform -csv ro parquet
    output location:`s3://bucket/sales_parquet`
    iamrole -AWSGLUESERVICEROLE
    scrip-autogrenraret

```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource0 = glueContext.create_dynamic_frame.from_catalog(
    database="sales_demo_db",
    table_name="sales_sales"
)
datasink1 = glueContext.write_dynamic_frame.from_options(
    frame=datasource0,
    connection_type="s3",
    connection_options={"path": "s3://my-de-lake-animesh11/sales_parquet/"},
    format="parquet"
)
job.commit()
```


another crawler required for parquet output ,to detect data schema from parquet table.

all set !!!🚀


# schema evolution(when column change over time)
soruce data changes,columns add/remove,datatype changes(str ->int)
so datalake should be configured in a way to adapt automatically without breaking etl job or athena queries

crawler do everything on own,like on adding new column in data ,crawler will update the same in everyplace.and similarly when parquet crawler runs it automatically updates parquet data 
table schema

,downstream jobs must be desgined to tolerate nulls.

---
# Partition Projection
normally;
   We upload new folder in s3,and then crawler must be run again to detect new partitions

Beccause problem is crawler cost money,slow for large data lakes,may fails if add thousand of partitions,not ideal for streaming inserts

partition project remove all of this.
athena is capable of generating partition at query time,without let storing anything in glue and without crawling

so wroking exmple is:

  S3 folder structure looks like
  ```
 s3://bucket/sales/year=2025/month=01/sales.csv
  s3://bucket/sales/year=2025/month=01/sales.csv
  ```
so crawler was used to detect year and month but no to avooid that confugiring glue table so athena utomatically knows valid years ,months,file format,s3 path pattern.

so basically instead of storing the partitions in  glue data catalog ,we tell athena the partition pattern to use during sql query execution.
crawler must run once to create table schema and rest of the time for partition part cna be done by **partition projection pattern** .
ATHENA DDL can be used to create external table by defining the strucutre of table 
for example:
Example 1: CSV table (with partition projection)
S3 layout
```sql
s3://sales-bucket/sales_csv/
  year=2024/month=09/day=01/
    data.csv
```
---

```
1Athena DDL (CSV)

CREATE EXTERNAL TABLE IF NOT EXISTS sales_csv (
  order_id      string,
  customer_id   string,
  amount        double,
  order_status  string
)
PARTITIONED BY (
  year  int,
  month int,
  day   int
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar'     = '"',
  'escapeChar'    = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://sales-bucket/sales_csv/'
TBLPROPERTIES (
  'skip.header.line.count' = '1',
  'projection.enabled' = 'true',

  'projection.year.type' = 'integer',
  'projection.year.range' = '2023,2026',

  'projection.month.type' = 'integer',
  'projection.month.range' = '1,12',
  'projection.month.digits' = '2',

  'projection.day.type' = 'integer',
  'projection.day.range' = '1,31',
  'projection.day.digits' = '2',

  'storage.location.template' =
    's3://sales-bucket/sales_csv/year=${year}/month=${month}/day=${day}/'
);
```
Query (CSV)

SELECT *
FROM sales_csv
WHERE year=2024 AND month=9 AND day=1;


---
✅ Example 2: Parquet table (with partition projection)

S3 layout

s3://sales-bucket/sales_parquet/
  year=2024/month=09/day=01/
    part-0001.parquet


---

Athena DDL (Parquet)
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS sales_parquet (
  order_id      string,
  customer_id   string,
  amount        double,
  order_status  string
)
PARTITIONED BY (
  year  int,
  month int,
  day   int
)
STORED AS PARQUET
LOCATION 's3://sales-bucket/sales_parquet/'
TBLPROPERTIES (
  'projection.enabled' = 'true',

  'projection.year.type' = 'integer',
  'projection.year.range' = '2023,2026',

  'projection.month.type' = 'integer',
  'projection.month.range' = '1,12',
  'projection.month.digits' = '2',

  'projection.day.type' = 'integer',
  'projection.day.range' = '1,31',
  'projection.day.digits' = '2',

  'storage.location.template' =
    's3://sales-bucket/sales_parquet/year=${year}/month=${month}/day=${day}/'
);

```
---

Query (Parquet)
```sql
SELECT order_id, amount
FROM sales_parquet
WHERE year=2024 AND month=9 AND day=1;
```
---

**note projection reure trict uqery discipline**
so need not to be used when
parittion range is very large like
year:2000-2100
month 1-12
day 1-31
total combination would be 100x12x31 =37200 partitions

it will make the query eventually slow and increase query planning time.

use it whwrever partition is patternet alwways not changes .so it better to use 
so its good when time base dparttions,large numbe rof partitions,append only datamstable schema,athena haeavy workload
