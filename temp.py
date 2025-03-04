import json

data = ['1740497815392674560',
        '{"level": "WARNING", "message": "2025-02-25 15:36:55,392 - WARNING - {\\"user_id\\": 52, \\"product_id\\": 1355, \\"amount\\": 62.53, \\"status\\": \\"success\\", \\"random_string\\": \\"0tDefqntLa\\"}", "timestamp": "2025-02-25 15:36:55"}']

# Extract ID
log_id = data[0]

# Parse the outer JSON
log_data = json.loads(data[1])

# Extract the 'message' field and parse the nested JSON inside it
message_part = log_data['message'].split(' - ')[-1]  # Extracting the actual JSON string
nested_data = json.loads(message_part)  # Parse it as JSON

# Print extracted values
print("Log ID:", log_id)
print("Level:", log_data["level"])
print("Timestamp:", log_data["timestamp"])
print("User ID:", nested_data["user_id"])
print("Product ID:", nested_data["product_id"])
print("Amount:", nested_data["amount"])
print("Status:", nested_data["status"])
print("Random String:", nested_data["random_string"])
