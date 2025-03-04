import logging
import json
import time
import requests
# Loki URL
LOKI_URL = "http://loki:3100/loki/api/v1/push"

# Function to send logs to Loki
def send_log_to_loki(level, message):
    try:
        log_entry = {
            "streams": [
                {
                    "stream": {"job": "python_script"},
                    "values": [[str(int(time.time() * 1e9)), json.dumps({
                        "level": level.upper(),
                        "message": message,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    })]]
                }
            ]
        }
        response = requests.post(
            LOKI_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(log_entry)
        )

        if response.status_code == 204:
            print(f"✅ Log sent: {message}")
        else:
            print(f"❌ Failed to send log: {response.text}")

    except Exception as e:
        print(f"Exception caught: {e}")

# Custom log handler to send logs to Loki
class LokiHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        send_log_to_loki(record.levelname, log_entry)

# Function to configure logging
def setup_logger(name="MyLogger", log_file="logs.txt"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all log levels

    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Console Handler (Print to console)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File Handler (Save to file)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Loki Handler (Send to Loki)
    loki_handler = LokiHandler()
    loki_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(loki_handler)

    return logger
