from pyspark.sql import SparkSession
import os

os.environ["PYSPARK_PYTHON"] = "C:/Users/lgeil.IL-MF10-NB100TS/Miniconda3/envs/myenv/python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = "C:/Users/lgeil.IL-MF10-NB100TS/Miniconda3/envs/myenv/python.exe"

spark = SparkSession.builder.master("local").appName("test").getOrCreate()
data = [("John", 1), ("Jane", 2)]
df = spark.createDataFrame(data, ["name", "id"])
df.show()





