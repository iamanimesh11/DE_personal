import requests
import time

loki_address = "http://localhost:3100"  # Replace with your Loki address
query = '{job="python_script"}'
start_time = int((time.time() - 3600) * 1e9)  # 1 hour ago (in nanoseconds)
end_time = int(time.time() * 1e9)  # Now (in nanoseconds)

url = f"{loki_address}/loki/api/v1/query_range?query={query}&start={start_time}&end={end_time}"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    data = response.json()
    print(f"data : {data}")
    # Process the data (log entries)
    for result in data["data"]["result"]:
        for stream in result["values"]:
          timestamp = int(stream[0])/1e9
          log_line = stream[1]
          print(f"[{timestamp}] {log_line}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
except KeyError as e:
    print(f"error parsing the json response: {e}")
