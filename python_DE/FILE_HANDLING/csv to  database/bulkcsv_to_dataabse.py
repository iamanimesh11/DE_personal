import datetime
import time
from plyer import notification

import mysql.connector
import csv

# Step 1: MySQL database connection details
db_config = {
    'user': 'root',
    'password': '@Nimesh11',
    'host': 'localhost',
    'database': 'trialmydatabase'
}

# Step 2: Connect to MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
# cursor = conn.cursor()
cursor.execute('''
       CREATE TABLE IF NOT EXISTS employees (
            Name VARCHAR(255) PRIMARY KEY,  -- Ensuring Name is unique
            Age INT,
            email varchar(255),
            Department VARCHAR(255),
            Salary INT
        )
    ''')

bulk_sizec = 100000
rows_to_insert = []
seen = set()
unique_rows = []
with open("random_data.csv", "r") as file:
    reader = csv.DictReader(file)
    reader.fieldnames = [header.strip() for header in reader.fieldnames]
    count = 0
    o_c = 0
    # name_V = [row['Name'] for row in  reader]
    # unique_name_values = set(name_V)
    # duplicate_count = len(name_V) - len(unique_name_values)
    # print("Number of duplicate 'name' values:", duplicate_count)
    t = datetime.datetime.now()
    for row in reader:
        o_c += 1
        name_age_tuple = (row['Name'], row['Age'])

        if name_age_tuple not in seen:
            if count % 100000 == 0:
                print(count)

            seen.add(name_age_tuple)  # Mark this Name-Age combination as seen
            rows_to_insert.append(
                (row['Name'], row['Age'], row['Email'], row['Department'], row['Salary'])
            )
            if len(rows_to_insert) == bulk_sizec:
                try:
                    cursor.executemany('''  
                        INSERT IGNORE INTO  employees(Name,Age,email,Department,Salary)
                        VALUES (%s,%s,%s,%s,%s)
                        ''', rows_to_insert)
                    conn.commit()
                    count += len(rows_to_insert)
                    rows_to_insert = []

                except mysql.connector.Error as err:
                    print(f"Error:{err}")
                    conn.rollback()
                    continue

# Step 6: Insert any remaining rows that didn't complete the last batch
if rows_to_insert:
    try:
        cursor.executemany('''
            INSERT IGNORE INTO employees (Name, Age, email, Department, Salary)
            VALUES (%s, %s, %s, %s, %s)
        ''', rows_to_insert)
        conn.commit()
        count += len(rows_to_insert)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()

print(datetime.datetime.now() - t)
print(count)
print(o_c)
conn.close()
notification.notify(
    title='csv to database',
    message='process completed.',
    app_name='My App',
    timeout=20  # Duration in seconds
)
