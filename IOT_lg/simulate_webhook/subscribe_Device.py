import psycopg2
import requests
import logging
import re
from datetime import datetime, timedelta
from Database_connection import connect_Database

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

db_connection = connect_Database()
cur = db_connection.cursor()

BASE_URL = "https://thinq.developer.lge.com/api"
AUTH_TOKEN = "your_access_token"

HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "x-country-code": "KR",
    "x-message-id": "0123456789012345678912",
    "x-service-id": "your_service_id",
    "x-service-key": "your_service_key",
    "Content-Type": "application/json"
}
# Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS iot_lg.devices_subscription_log (
        device_id VARCHAR(255) PRIMARY KEY,
        subscribed BOOLEAN DEFAULT FALSE,
        webhook_url TEXT,
        timestamp TIMESTAMP DEFAULT NOW()
    );
""")

db_connection.commit()

# Fetch devices

cur.execute("""
    SELECT  device_type, model_name FROM iot_lg.all_table_names;
""")

unique_devices = cur.fetchall()

for device_type, model_name in unique_devices:
    if device_type!="DEVICE_REFRIGERATOR":
        continue
    table_name = f"{device_type.lower().replace('device_', '')}_model_{model_name.lower()}"
    table_name = re.sub(r'\W+', '_', table_name)  # Replace non-word characters with '_'
    table_name = table_name.strip('_')
    print(table_name)

    query=f"""
    SELECT device_id FROM iot_lg.{table_name}"""

    cur.execute(query)
    devices = cur.fetchall()


    for device in devices:
        device_id = device[0]
        subscription_duration_hours = 24

        try:
            url = f"{BASE_URL}/event/{device_id}"
            payload = {"expire": {"unit": "HOUR", "timer": subscription_duration_hours}}
            expiration_time = datetime.now() + timedelta(hours=subscription_duration_hours)

            response = requests.post(url, headers=HEADERS,json=payload,timeout=10)
            response.raise_for_status()  # Raises an error

            if response.status_code == 200:
                # **Update `subscribed` and `webhook_url` in the same table**
                update_query = f"""
                               UPDATE iot_lg.{table_name}
                               SET subscription_status = TRUE, 
                                    webhook_url = %s,
                                    subscription_time = NOW(),
                                    subscription_expiration = %s
                               WHERE device_id = %s;
                                """
                cur.execute(update_query,(url,expiration_time,device_id))
                db_connection.commit()
                logging.info(f"Subscribed {device_id} to webhook.")

            else:
                logging.warning(f"Failed to subscribe {device_id}, response: {response.text}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error subscribing {device_id}: {e}")

cur.close()
db_connection.close()
