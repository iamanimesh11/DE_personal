# Import findspark
import findspark
findspark.init()
from pyspark.sql import  row
row = Row(name='q', age=25, city='India')

# Access the values of the row using dot notation
print(row.name)
print(row.age)
print(row.city)


