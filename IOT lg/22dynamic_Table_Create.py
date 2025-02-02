import psycopg2
import io
import logging
from psycopg2 import extensions

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="de_personal",  # Replace with your actual DB name
    user="postgres",       # Replace with your actual DB user
    password="animesh11",  # Replace with your actual password
    host="localhost",      # Replace with your DB host if necessary
    port="5432"            # Default PostgreSQL port
)
cur = conn.cursor()

# Step 2: Ensure the 'devices' schema exists, create it if it doesn't
try:
    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS devices;
    """)
    conn.commit()
    logging.info("Schema 'devices' exists or was created successfully.")
except Exception as e:
    logging.error(f"Error while creating schema: {e}")

# Step 3: Create the 'devices2' table inside the 'devices' schema
try:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS devices.devices2 (
            device_id UUID PRIMARY KEY,
            device_type TEXT,
            model_name TEXT,
            alias TEXT,
            reportable BOOLEAN
        );
    """)
    conn.commit()
    logging.info("Table 'devices2' created inside 'devices' schema successfully.")
except Exception as e:
    logging.error(f"Error while creating table devices2: {e}")

# Step 4: Set the search path to the 'devices' schema
cur.execute("SET search_path TO devices;")
conn.commit()

# Step 5: Create a sample in-memory CSV using StringIO
csv_data = io.StringIO()

# Write the CSV header (without created_at and updated_at columns)
csv_data.write("device_id,device_type,model_name,alias,reportable\n")

# Write some sample device data (without created_at and updated_at)
csv_data.write("A431F0FD-8214-4029-A9FB-6126B40BD272,DEVICE_REFRIGERATOR,FrostMaster,Kitchen Fridge,True\n")
csv_data.write("B431F0FD-8214-4029-A9FB-6126B40BD273,DEVICE_WASHING_MACHINE,WM-X,Living Room AC,True\n")
csv_data.write("C431F0FD-8214-4029-A9FB-6126B40BD274,DEVICE_AIR_CONDITIONER,AC-123,Office AC,False\n")

# Rewind the StringIO object to the beginning (so we can read from it)
csv_data.seek(0)

# Step 6: Skip the header row
csv_data.readline()  # Skips the first line (header)

# Step 7: Insert data into the 'devices2' table inside the 'devices' schema
table_name = "devices2"  # The target table in the 'devices' schema
try:
    # Use copy_from to load the CSV data into the table 'devices2'
    cur.copy_from(csv_data, table_name, sep=',', columns=(
        'device_id', 'device_type', 'model_name', 'alias', 'reportable'))

    # Commit the transaction
    conn.commit()
    logging.info("Data inserted successfully into the devices2 table inside the 'devices' schema.")

except Exception as e:
    logging.error(f"Error during bulk insert: {e}")
    conn.rollback()  # Rollback in case of an error

# Step 8: Verify the insertion (optional)
cur.execute("SELECT * FROM devices.devices2")  # Query the new table
rows = cur.fetchall()
for row in rows:
    logging.info(row)

# Step 9: Close the connection
cur.close()
conn.close()
