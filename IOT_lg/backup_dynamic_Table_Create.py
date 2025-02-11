
import psycopg2
import io
import re
import logging
import json
import time
start_time=time.time()
from Database_connection import connect_Database
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to DB
db_connection= connect_Database()
cur = db_connection.cursor()

# Load data from the JSON file
with open('devices.json', 'r') as file:
    api_response = json.load(file)


# Function to check if a table exists for device type and model
checked_tables = set()

def check_table_exists(table_name):
    table_name="device_staging"
    if table_name in checked_tables:
        return True
    cur.execute("""
        SELECT 1
        FROM information_schema.tables 
        WHERE table_schema = 'iot_lg' 
        AND table_name = %s
    """, (table_name,))
    exists = cur.fetchone() is not None
    if exists:
        checked_tables.add(table_name)
    return exists

# Function to create a table dynamically if not exists
def create_table(table_name):
    table_name="device_staging"
    create_query = f"""
        CREATE TABLE IF NOT EXISTS iot_lg.{table_name} (
            device_id VARCHAR(255) PRIMARY KEY,
            device_type VARCHAR(50) NOT NULL,
            model_name VARCHAR(255) NOT NULL,
            alias VARCHAR(255),
            is_active BOOLEAN DEFAULT TRUE,
            reportable BOOLEAN DEFAULT TRUE,
            subscription_status BOOLEAN DEFAULT FALSE,
            log_action TEXT DEFAULT 'inserted',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
    """
    cur.execute(create_query)
    db_connection.commit()
    print(f"✅ Created table: {table_name}")


# Function to insert device data into its corresponding table
# Now process the devices one by one


csv_data = io.StringIO()
batch_size=2000
# Initialize a dictionary to group devices by table_name
devices_by_table = {}
log_printed=False
# Process each device from the API response
for device in api_response['response']:
    device_id = device['deviceId']
    device_type = device['deviceInfo']['deviceType']
    model_name = device['deviceInfo']['modelName']
    alias = device['deviceInfo']['alias']
    reportable = device['deviceInfo']['reportable']
    table_name = f"{device_type.lower().replace('device_', '')}_model_{model_name.lower()}"
    table_name = re.sub(r'\W+', '_', table_name)  # Replace non-word characters with '_'
    table_name=table_name.strip('_')

    # Check if table exists for device type and model name
    table_Exist =check_table_exists(table_name)
    if table_Exist :
        if not log_printed:
            print(f"Table {table_name}  already exists!")
            log_printed=True

    if not table_Exist:
       print(f"Table {table_name} doesn't  exists ,creating!")
       create_table(table_name)

    # Group devices by table_name
    if table_name not in devices_by_table:
            devices_by_table[table_name] = []
    devices_by_table[table_name].append((device_id, device_type, model_name, alias, reportable))

# Step 4: Set the search path to the 'devices' schema
cur.execute("SET search_path TO iot_lg;")
db_connection.commit()
# Process each table's devices in batches
for table_name, devices in devices_by_table.items():
    logging.debug(f"Processing table: {table_name}")

    try:
        # Prepare in-memory CSV for each table
        csv_data = io.StringIO()
        count = 0

        # Process the devices for this table in batches
        for device in devices:
            device_id, device_type, model_name, alias, reportable = device
            created_at = "NULL"  # Placeholder if you want NULL or let PostgreSQL handle this
            updated_at = "NULL"  # Same for updated_at

            # logging.debug(f"Preparing data for device_id: {device_id}, device_type: {device_type}, model_name: {model_name}")

            csv_data.write(f"{device_id},{device_type},{model_name},{alias},{reportable}\n")
            count += 1

            # Once we reach the batch size, load the data into the database
            if count >= batch_size:
                logging.debug(f"Batch size reached, inserting batch for table: {table_name}")

                csv_data.seek(0)
                quoted_table_name = psycopg2.extensions.quote_ident(f'devices.{table_name}',db_connection)  # Quote table name


                cur.copy_from(csv_data, "device_staging", sep=',', columns=(
                    'device_id', 'device_type', 'model_name', 'alias', 'reportable'))

                db_connection.commit()
                logging.info(f"Batch inserted for {table_name}, {count} records.")

                csv_data.seek(0)
                csv_data.truncate(0)  # Clear the in-memory CSV for the next batch
                count = 0

        # Insert any remaining records for this table (less than batch_size)
        if count > 0:

            # Move the cursor to the beginning of the StringIO buffer
            csv_data.seek(0)

            # Logging for debugging (check csv content if needed)
            try:
                logging.debug(f"Inserting remaining {count} records into table: {table_name}")
                # Check if the table exists before inserting
                cur.execute("""
                    SELECT EXISTS (
                        SELECT 1
                        FROM information_schema.tables
                        WHERE table_schema = 'iot_lg'
                        AND table_name = %s
                    );
                """, (table_name,))
                exists = cur.fetchone()[0]

                if not exists:
                    logging.error(f"Table {table_name} does not exist!")
                    # Handle this case (e.g., create the table or log the error)

                # Insert the data from csv_data into the table
                cur.copy_from(csv_data, "device_staging", sep=',', columns=(
                    'device_id', 'device_type', 'model_name', 'alias', 'reportable'))

                # Commit the transaction once the data is inserted
                db_connection.commit()

                # Clear csv_data to free up memory and reset it for future use
                csv_data.seek(0)
                csv_data.truncate(0)

                logging.info(f"Remaining records inserted for {table_name}, {count} records.")

            except Exception as e:
                # In case of an error, log the exception
                logging.error(f"Error inserting remaining records for {table_name}: {e}")
                db_connection.rollback()  # Rollback the transaction in case of error


    except Exception as e:
        logging.error(f"Error processing batch for {table_name}: {e}")
        logging.error(f"Device data: {device}")



# Close connection
cur.close()
db_connection.close()
end_Time=time.time()
print(f"total time taken : {end_Time-start_time} seconds")
