
from pyspark.sql import SparkSession
spark=SparkSession.builder.master("local").appName("first pyspark app").getOrCreate()

sc=spark.sparkContext

data=[1,2,3,4,5]
rdd=sc.parallelize(data)

rdd_transformed =rdd.map(lambda x: x*2)
result=rdd_transformed.collect()
print("tranformed: ",result)
spark.stop()

# lf
