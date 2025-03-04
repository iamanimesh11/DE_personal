import streamlit as st
import requests
import pandas as pd
import subprocess
import time
import os
from datetime import datetime
import json
# Loki Query URL (update if needed)
LOKI_QUERY_URL = "http://loki:3100/loki/api/v1/query_range"

st.title("📊Log r ")
st.markdown("Click **Start Sending Logs** to begin logging.")
st.sidebar.markdown("🔗 [Open  Grafana Dashboard](http://localhost:3000)")

st.sidebar.title("find here ,gafrana")
if "log_process" not in st.session_state:
    st.session_state["log_process"] = None

# Function to start logging
def start_logging():
    if st.session_state["log_process"] is None:
        st.session_state["log_process"] = subprocess.Popen(["python", "logSentToLoki.py"])
        st.success("✅ Logging started!")

# Function to stop logging
def stop_logging():
    if st.session_state["log_process"] is not None:
        st.session_state["log_process"].terminate()
        st.session_state["log_process"] = None
        st.warning("🛑 Logging stopped!")

# Function to fetch logs from Loki
def fetch_logs():
    query = '{job="python_script"}'
    params = {
        "query": query,
        "limit": 50,
        "direction": "backward",
        "step": "10s",
    }

    try:
        response = requests.get(LOKI_QUERY_URL, params=params)
        data = response.json()
        logs = []

        # Parse logs
        for stream in data.get("data", {}).get("result", []):
            for entry in stream.get("values", []):
                log_id = entry[0]  # Timestamp or log ID
                log_message = entry[1]  # Log message (JSON string)

                try:
                    log_data = json.loads(log_message)  # Parse the outer JSON

                    # Extract the 'message' field and parse the nested JSON inside it
                    message_part = log_data["message"].split(" - ")[-1]  # Get JSON string
                    nested_data = json.loads(message_part)  # Parse it
                    # Store extracted values
                    logs.append({
                        "log_id": log_id,
                        "Level": log_data.get("level", "UNKNOWN"),
                    "User ID": nested_data.get("user_id", "N/A"),
                    "Product ID": nested_data.get("product_id", "N/A"),
                    "Amount": nested_data.get("amount", "N/A"),
                    "Status": nested_data.get("status", "N/A"),
                    "Random String": nested_data.get("random_string", "N/A"),
                    })

                except json.JSONDecodeError:
                    st.warning(f"Failed to parse log message: {log_message}")
        return pd.DataFrame(logs)

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch logs: {e}")
        return pd.DataFrame()

# Streamlit Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Start Sending Logs"):
        start_logging()
with col2:
    if st.button("🛑 Stop Logging"):
        stop_logging()

# Fetch logs when button is clicked
if st.button("🔄 Refresh Logs"):
    logs_df = fetch_logs()
    if not logs_df.empty:
        st.dataframe(logs_df, use_container_width=True)
    else:
        st.warning("No logs found. Make sure logging is running.")

