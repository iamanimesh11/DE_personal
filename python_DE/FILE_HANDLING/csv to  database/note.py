# 1 Pandas (Standard for Small to Medium-sized CSVs)


import pandas as pd
df = pd.read_csv('file.csv')
# chunk based in pandas

df_chunk = pd.read_csv('file.csv', chunksize=100000)
for chunk in df_chunk:
    process(chunk)

# 2. Dask (For Large Datasets, Parallel Processing)
import dask.dataframe as dd
df = dd.read_csv('file.csv')

# 3. PyArrow (For High Performance and Memory Efficiency)
import pyarrow.csv as pv
table = pv.read_csv('file.csv')

# 4. CSV Reader (For Low-level Efficient File Streaming)
import csv
with open('file.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        process(row)

# //5. Modin (Parallel Processing Using Pandas API)
import modin.pandas as pd
df = pd.read_csv('file.csv')

# 6. Vaex (For Huge Datasets, Out-of-core Processing)
import vaex
df = vaex.from_csv('file.csv')


# Small to Medium CSVs (< 1-2 GB): Use pandas.read_csv().
# Medium to Large CSVs (1 GB to 10 GB): Use pandas with chunksize or Modin.
# Large Datasets (10+ GB): Use Dask, PyArrow, or Vaex.
# Low-memory/Stream Processing: Use csv.reader or Dask.






# 0:02:19.322149
# 458858
# 1926000
#
#
# 0:09:40.930085    on 10,000 single way
# 1726261
# 1926000
#
# 0:01:25.141136    on bulk 1000
# 1726261
# 1926000
#
# 0:01:14.274447    on bulk 10000
# 1726261
# 1926000
#
# 0:01:06.974990    on bulk 100,000
# 1726261
# 1926000