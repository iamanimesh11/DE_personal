import requests
import logging
import json
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(["http://localhost:9200"])


def log_to_elasticsearch(index, log_data):
    es.index(index=index, body=log_data)


# Subscription example
device_id = "device_12345"
url = f"https://thinq.developer.lge.com/api/event/{device_id}"
payload = {"expire": {"unit": "HOUR", "timer": 24}}

try:
    response = requests.post(url, json=payload)
    response.raise_for_status()

    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "device_id": device_id,
        "subscription_status": "success",
        "response_time": response.elapsed.total_seconds()
    }

except requests.exceptions.RequestException as e:
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "device_id": device_id,
        "subscription_status": "failed",
        "error_message": str(e)
    }

# Send log to Elasticsearch
log_to_elasticsearch("subscription_logs", log_data)
