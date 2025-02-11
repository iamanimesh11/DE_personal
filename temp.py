WEBHOOK_MAPPING = {
    "refrigerator": "http://localhost:8000/refrigerator-events/",
    "washer": "http://localhost:8000/washer-events/",
    "air_conditioner": "http://localhost:8000/ac-events/"
}
device_type="refrigerator"
webhook_url = WEBHOOK_MAPPING.get(device_type, "http://localhost:8000/default-events/")
print(webhook_url)