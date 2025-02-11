import uuid
import random
import json
from datetime import datetime
import psycopg2

postgres_params = {
    "host": "localhost",
    "database": "de_personal",
    "user": "airflow_user",
    "password": "animesh11"
}

# Function to generate random device data and
def generate_device_data(num_devices=100):
    device_data = []
    device_types = ["DEVICE_REFRIGERATOR", "DEVICE_WASHER", "DEVICE_AIR_PURIFIER", "DEVICE_OVEN"]
    # Define model names based on device type
    model_options = {
        "DEVICE_REFRIGERATOR": ["r1", "r2", "r3"],
        "DEVICE_WASHER": ["m1", "m2", "m3"],
        "DEVICE_AIR_PURIFIER": ["a1", "a2", "a3"],
        "DEVICE_OVEN": ["o1", "o2", "o3"]
    }

    for _ in range(num_devices):
        device_type = random.choice(device_types)
        device = {
            "messageId": str(random.randint(1000000000000000000000, 9999999999999999999999)),
            "timestamp": datetime.now().isoformat(),
            "response": [{
                "deviceId": str(uuid.uuid4()),
                "deviceInfo": {
                    "deviceType": device_type,
                    "modelName": random.choice(model_options[device_type]),  # Choose model based on device type
                    "alias": f"nickname_{random.randint(1, 100)}",
                    "reportable": random.choice([True, False])
                }
            }]
        }
        device_data.append(device)

    return device_data

device_data = generate_device_data(10)

# Write the data to a JSON file
with open('device_data.json', 'w') as f:
    json.dump(device_data, f, indent=4)

print("File 'device_data.json' created with 100 random devices.")


# def get_Db_connection(num_devices=100):
#     device_data=[]
#     device_types = ["DEVICE_REFRIGERATOR", "DEVICE_WASHER", "DEVICE_AIR_PURIFIER", "DEVICE_OVEN"]
#     # Define model names based on device type
#     model_options = {
#         "DEVICE_REFRIGERATOR": ["r1", "r2", "r3"],
#         "DEVICE_WASHER": ["m1", "m2", "m3"],
#         "DEVICE_AIR_PURIFIER": ["a1", "a2", "a3"],
#         "DEVICE_OVEN": ["o1", "o2", "o3"]
#     }
#     for _ in range(num_devices):
#         device_type = random.choice(device_types)
#
