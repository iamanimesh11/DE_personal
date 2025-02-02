import random
import uuid
import json
from collections import defaultdict

# Example lists of device types and model names (you can expand these lists as needed)
device_types = ["DEVICE_REFRIGERATOR", "DEVICE_AIR_CONDITIONER", "DEVICE_WASHING_MACHINE", "DEVICE_TV", "DEVICE_MICROWAVE"]
model_names = {
    "DEVICE_REFRIGERATOR": ["S-TF", "FrostMaster", "CoolWave"],
    "DEVICE_AIR_CONDITIONER": ["AC-123", "CoolBreeze", "AirMax"],
    "DEVICE_WASHING_MACHINE": ["WM-XYZ", "WashPro", "SpinMaster"],
    "DEVICE_TV": ["UltraView", "CinemaMax", "ScreenPro"],
    "DEVICE_MICROWAVE": ["MicroWaveX", "QuickHeat", "HeatMaster"]
}

# Function to generate random device info
def generate_random_device():
    device_type = random.choice(device_types)
    model_name = random.choice(model_names[device_type])
    device_id = str(uuid.uuid4()).upper()
    alias = f"{device_type.split('_')[1]}_{model_name}"
    return {
        "deviceId": device_id,
        "deviceInfo": {
            "deviceType": device_type,
            "modelName": model_name,
            "alias": alias,
            "reportable": True
        }
    }

# Generate 100 random devices
devices = [generate_random_device() for _ in range(2)]
print(devices)
# Group devices by deviceType and modelName
grouped_devices = defaultdict(list)
for device in devices:
    device_type = device["deviceInfo"]["deviceType"]
    model_name = device["deviceInfo"]["modelName"]
    grouped_devices[(device_type, model_name)].append(device)

# Create an empty list to hold all the devices
response = []

# Loop over each device list in the grouped_devices dictionary
for device_list in grouped_devices.values():
    # Loop over each individual device in the current device list
    for device in device_list:
        # Add the device to the response list
        response.append(device)


# Prepare the API response
api_response = {
    "messageId": str(uuid.uuid4()).replace("-", "")[:24],
    "timestamp": "2024-10-27T11:15:00.123456",
    "response":response
}


# Save the response to a JSON file
output_filename = "devices.json"
with open(output_filename, 'w') as json_file:
    json.dump(api_response, json_file, indent=4)

print(f"Data has been saved to {output_filename}")
