import datetime
import dask.dataframe as dd
import pandas as pd
import csv
import modin.pandas as mpd
import time
import psutil
import os
import tracemalloc

process = psutil.Process(os.getpid())
def memory_usage():
    # Returns the memory used by the current process in MB
    return process.memory_info().rss / (1024 * 1024)


def comparison_time(name):
    print(f"Starting '{name}' method... ")
    # initial_mem = memory_usage()
    tracemalloc.start()

    t = time.perf_counter()
    match name:
        case "pandas":
            df = pd.read_csv('random_data.csv')
            rows=len(df)
            print(f"Rows: {len(df)}")

        case "chunk_pandas":
            df_chunk = pd.read_csv('random_data.csv', chunksize=1000)
            count = 0
            for chunk in df_chunk:
                count += len(chunk)
            rows=count
            print(f"Rows: {count}")

        case "dask":
            df = dd.read_csv('random_data.csv')
            rows=len(df)
            print(f"Rows (lazy): {len(df)}")  # Dask lazily evaluates, so this may trigger computations

        case "csv_Reader":
            with open('random_data.csv', mode='r') as file:
                csv_reader = csv.reader(file)
                count = 0
                for row in csv_reader:
                    count += 1
            rows=count
            print(f"Rows: {count}")

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    # Convert memory usage from bytes to MB
    initial_mem_mb = current / (1024 * 1024)
    peak_mem_mb = peak / (1024 * 1024)

    print(f"Time elapsed: {time.perf_counter() - t:.4f} seconds")
    # print(f"Memory after execution: {memory_usage():.2f} MB")
    print(f"initial_mem_mb:{initial_mem_mb:.2f} MB ,peak : {peak_mem_mb:.2f}")
    time_elapsed = time.perf_counter() - t
    final_mem = memory_usage()


    return name, rows, time_elapsed, initial_mem_mb, final_mem

# Function to write results to CSV

l =["pandas","csv_Reader","dask","chunk_pandas"]

for i in l:
    print(i)
    results=comparison_time(i)
    print('-' * 50)




