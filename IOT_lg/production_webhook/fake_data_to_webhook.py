import requests

# Define the fake event data (mimicking the actual structure)
fake_event = {
    "event": {
        "deviceId": "123e4567-e89b-12d3-a456-426614174000",  # Example device ID (UUID-like)
        "pushType": "error",  # Example event type
        "deviceType": "Refrigerator",  # Simulate a Refrigerator event
        "report": {
            "error": "Temperature sensor failure"  # Simulate an error in the event
        }
    }
}

# Define the webhook URL (replace with your ngrok or live server URL)
webhook_url = "http://127.0.0.1:8000/device-event"  # Local server URL for testing

# Send the POST request to your webhook server
response = requests.post(webhook_url, json=fake_event)

# Print the response from the server
print(f"Response Status: {response.status_code}")
print(f"Response Body: {response.text}")
