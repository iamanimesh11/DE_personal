import time
import json
import logging
import requests
import random
import string
import re
# Loki URL
LOKI_URL = "http://localhost:3100/loki/api/v1/push"

# Set up logging
logger = logging.getLogger("LokiLogger")
logger.setLevel(logging.DEBUG)
import json
import re

def extract_json_from_message(message):
    """
    Extracts a valid JSON object from a string if present, otherwise returns the original message.
    """
    match = re.search(r"\{.*\}", message)  # Look for a JSON-like structure
    if match:
        json_str = match.group()  # Extract potential JSON
        try:
            return json.loads(json_str)  # Validate and parse JSON
        except json.JSONDecodeError:
            pass  # If invalid, treat it as a normal string
    return message  # Return original if no valid JSON is found

# Function to send logs to Loki
def send_log_to_loki(level, message):
    print("message")
    print(message)
    extracted_message = extract_json_from_message(message)


    print("Extracted JSON:", extracted_message)  # Debugging

    job = random.choice(["python_Script 1", "python_script 2"])

    try:
        if isinstance(extracted_message, dict):
            log_message = extracted_message  # Use as is if it's already a dictionary
        else:
            log_message = {"message": extracted_message}  # Wrap non-JSON messages in a dict

        message_string = json.dumps(log_message)  # Ensures it's a JSON string


        log_entry = {
            "streams": [
                {
                    "stream": {"job": job},
                    "values": [[
                        str(int(time.time() * 1e9)),  # Timestamp in nanoseconds
                        json.dumps({
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),  # Readable timestamp
                            "job_name":job,
                            "level": level.upper(),
                            "message": message_string  # Everything inside "message"
                        })
                    ]]
                }
            ]
        }
        # print("Final log entry:", json.dumps(log_entry, indent=4))  # Debugging
        # time.sleep(20)
        response = requests.post(
            LOKI_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(log_entry)
        )

        if response.status_code == 204:
            print(f"✅ Log sent: {message_string}")
        else:
            print(f"❌ Failed to send log: {response.text}")

    except Exception as e:
        print(f"exception caught: {e}")

# Custom log handler to send logs to Loki
class LokiHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        send_log_to_loki(record.levelname, log_entry)

# Add LokiHandler to the logger
loki_handler = LokiHandler()
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
loki_handler.setFormatter(formatter)
logger.addHandler(loki_handler)


# Function to generate random string
def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# Function to generate random data
def generate_random_data():
    data = {
        "user_id": random.randint(1, 100),
        "product_id": random.randint(1000, 2000),
        "amount": round(random.uniform(10.0, 100.0), 2),
        "status": random.choice(["success", "failure", "pending"]),
        "random_string": generate_random_string()
    }
    return json.dumps(data)

# Logging random data loop
try:
    while True:
        log_level = random.choice(["INFO", "WARNING", "ERROR"])
        random_data = generate_random_data()

        if log_level == "INFO":
            logger.info(random_data)
        elif log_level == "WARNING":
            logger.warning(random_data)
        elif log_level == "ERROR":
            logger.error(random_data)

        time.sleep(random.uniform(0.5, 2.0))  # Log every 0.5 to 2 seconds

except KeyboardInterrupt:
    print("Logging stopped.")