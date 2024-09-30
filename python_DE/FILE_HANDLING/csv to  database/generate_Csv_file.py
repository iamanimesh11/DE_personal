import datetime
import random

import pandas as pd
import numpy as np
from faker import Faker
import os

# Initialize the Faker library
fake = Faker()
# Function to generate random data
def generate_random_data(rows, columns):
    departments =["HR","Finance","Marketing","Sales","Customer Service","IT","Legal"]
    data = {}
    for i in range(columns):
        print(i,columns)
        # Create different types of random data
        if i % 5 == 0:
            data[f"Name"] = [fake.name() for _ in range(rows)]  # Random names
        elif i % 5 == 1:
            data[f"Age"] = np.random.randint(1, 100, size=rows)  # Random numbers
        elif i % 5 == 2:
             data[f"Email"] = [fake.email() for _ in range(rows)]  # Random emails
        elif i % 5 == 3:
            data[f"Department"] = [random.choice(departments) for _ in range(rows)]  # Random emails
        elif i % 5 == 3:
            data[f"City"] = [fake.city() for _ in range(rows)]  # Random cities
        else:
            data[f"Salary"] = np.random.randint(0, 100000, size=rows)  # Random numbers
    return pd.DataFrame(data)


# Function to create a CSV file of the desired size
def create_csv_of_size(file_name, rows, columns, approx_file_size_mb):
    # Keep generating rows and saving the CSV until the file reaches the desired size
    print("create_Csv exected")
    total_size = 0
    chunk_size = 100000  # Save in chunks to avoid memory issues with large datasets
    chunk_rows = min(rows, chunk_size)

    # Generate the initial random data chunk
    df = generate_random_data(chunk_rows, columns)
    print("generate_random_data exected")

    df.to_csv(file_name, index=False, mode='w', header=True)

    # Keep appending more chunks until the file reaches the approximate desired size
    while os.path.getsize(file_name) / (1024 * 1024) < approx_file_size_mb:
        print(os.path.getsize(file_name) / (1024 * 1024))
        df = generate_random_data(chunk_rows, columns)
        df.to_csv(file_name, index=False, mode='a', header=False)  # Append mode

    print(f"CSV file '{file_name}' created with approximately {approx_file_size_mb} MB size.")


# Usage Example
rows = 1000 # Total number of rows (adjust based on file size requirement)
columns = 6  # Number of columns
approx_file_size_mb = 100  # Approximate file size in MB
file_name = "random_data.csv"
t=datetime.datetime.now
create_csv_of_size(file_name, rows, columns, approx_file_size_mb)
# print(datetime.datetime.now()-t)