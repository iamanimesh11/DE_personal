import streamlit as st
import requests
import time

st.set_page_config(page_title="📡 Service Status Dashboard", layout="wide")

# Define services and their healthcheck URLs and online logo URLs
SERVICES = {
    "Airflow": {
        "url": "http://airflow:8080/health",
        "description": "Workflow orchestration platform.",
        "logo": "https://icon.icepanel.io/Technology/svg/Apache-Airflow.svg",
        "restart_command": "docker restart airflow-container-name",
    },
    "Airflow Scheduler": {
        "url": "http://airflow:8080/health",
        "description": "Airflow component for scheduling tasks.",
        "logo": "https://icon.icepanel.io/Technology/svg/Apache-Airflow.svg",
    },
    "Airflow Webserver": {
        "url": "http://airflow:8080/health",
        "description": "Airflow UI for monitoring and managing workflows.",
        "logo": "https://icon.icepanel.io/Technology/svg/Apache-Airflow.svg",
    },
    "Kafka": {
        "url": "http://kafka:9092",
        "description": "Distributed event streaming platform.",
        "logo": "https://images.icon-icons.com/2699/PNG/512/apache_kafka_vertical_logo_icon_169585.png",
    },
    "Zookeeper": {
        "url": "http://zookeeper:2181",
        "description": "Centralized coordination service.",
        "logo": "https://hub.docker.com/api/media/repos_logo/v1/library%2Fzookeeper",
    },
    "Grafana": {
        "url": "http://grafana:3000",
        "description": "Data visualization and monitoring tool.",
        "logo": "https://www.skedler.com/blog/wp-content/uploads/2021/08/grafana-logo-768x384.png",
    },
    "Loki": {
        "url": "http://grafana:3000",
        "description": "Log aggregation system.",
        "logo": "https://image.pngaaa.com/608/4821608-middle.png",
    },
    "Postgres": {
        "url": "http://grafana:3000",
        "description": "Open-source relational database.",
        "logo": "https://www.logo.wine/a/logo/PostgreSQL/PostgreSQL-Logo.wine.svg",
    },
}
# Setup session state
for service in SERVICES:
    st.session_state.setdefault(f"{service}_status", "🔘 Not Checked")
    st.session_state.setdefault(f"{service}_color", "gray")
    st.session_state.setdefault(f"{service}_last_checked", "Never")
    st.session_state.setdefault(f"{service}_response", "")

# Inject card CSS with logo styling
st.markdown(f"""
    <style>
        div.card-container {{
            background-color: #e3f2fd;
            border-radius: 15px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            height: 200px; /* Increased height to accommodate logo and more content */
            display: flex;
            flex-direction: column;
            align-items: center; /* Center items horizontally */
        }}
        div.card-logo {{
            width: 150px; /* Adjust logo size as needed */
            height: 60px;
            margin-bottom: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        div.card-logo img {{
            max-width: 100%;
            max-height: 100%;
            border-radius: 10px; /* Optional: round the corners of the logo */
        }}
        div.card-title {{
            font-size: 18px;
            font-weight: 600;
            text-align: center;
                        color: black;

            margin-bottom: 5px;
        }}
        div.card-description {{
            font-size: 10px;
            color: #555;
            text-align: center;
            margin-bottom: 10px;
            overflow: hidden; /* To handle longer descriptions */
        }}
        div.card-status-container {{
            text-align: center;
            margin-top: auto; /* Push status to the bottom */
        }}
        div.card-status {{
            font-size: 20px;
        }}
        div.card-last-checked {{
            font-size: 10px;
            color: #777;
            text-align: center;
            margin-top: 3px;
        }}
        div.card-response {{
            font-size: 10px;
            color: white;
            overflow: auto;
            max-height: 100px;
            margin-top: 5px;
            background-color: black;
            padding: 5px;
            border-radius: 5px;
        }}
    </style>
""", unsafe_allow_html=True)

# Dashboard title
st.title("🐳 Docker Containers & Service Status")
st.markdown("A real-time dashboard to monitor the health of Docker containers and their internal services.")
st.markdown("---")
# === Sidebar Navigation ===
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["kafka", "postgres", "logs","p"])
# Calculate the number of columns needed
num_services = len(SERVICES)
num_cols = (num_services + 4) // 5  # Ensure at most 6 cards per row

# Create rows of columns
for i in range(num_cols):
    cols = st.columns(5)
    for j in range(5):
        index = i * 5 + j
        if index < num_services:
            name = list(SERVICES.keys())[index]
            service_info = SERVICES[name]
            url = service_info["url"]
            description = service_info["description"]
            logo_url = service_info["logo"]
            restart_command = service_info.get("restart_command", "No command available") # Get command, default if missing

            with cols[j]:
                with st.container():
                    # Start card wrapper
                    st.markdown(f'<div class="card-container"><div class="card-logo"><img src="{logo_url}" alt="{name} Logo"></div><div class="card-title">{name}</div><div class="card-description">{description}</div>', unsafe_allow_html=True)

                    # Button + logic
                    if st.button("Check Status", key=f"{name}_btn"):
                        with st.spinner(f"Checking {name}..."):
                            try:
                                start_time = time.time()
                                res = requests.get(url, timeout=5)
                                end_time = time.time()
                                response_time = f"{(end_time - start_time):.2f}s"
                                st.session_state[f"{name}_last_checked"] = time.strftime("%Y-%m-%d %H:%M:%S")
                                st.session_state[f"{name}_response"] = f"Status Code: {res.status_code}, Response Time: {response_time}"
                                if res.status_code == 200:
                                    st.session_state[f"{name}_status"] = "✅ Running"
                                    st.session_state[f"{name}_color"] = "green"
                                else:
                                    st.session_state[f"{name}_status"] = f"⚠️ Issue ({res.status_code})"
                                    st.session_state[f"{name}_color"] = "orange"
                            except requests.exceptions.RequestException as e:
                                st.session_state[f"{name}_status"] = "❌ Down"
                                st.session_state[f"{name}_color"] = "red"
                                st.session_state[f"{name}_last_checked"] = time.strftime("%Y-%m-%d %H:%M:%S")
                                st.session_state[f"{name}_response"] = f"Error: {e}"
                            except Exception as e:
                                st.session_state[f"{name}_status"] = "❓ Unknown Error"
                                st.session_state[f"{name}_color"] = "gray"
                                st.session_state[f"{name}_last_checked"] = time.strftime("%Y-%m-%d %H:%M:%S")
                                st.session_state[f"{name}_response"] = f"Unexpected Error: {e}"

                    # Status Container
                    st.markdown(f'<div class="card-status-container">', unsafe_allow_html=True)
                    status = st.session_state[f"{name}_status"]
                    color = st.session_state[f"{name}_color"]
                    st.markdown(
                        f'<div class="card-status" style="color:{color}">{status}</div>',
                        unsafe_allow_html=True
                    )
                 
                    st.markdown(
                        f'<div class="card-last-checked">Last Checked: {st.session_state[f"{name}_last_checked"]}</div>',
                        unsafe_allow_html=True
                    )
                    if status =="❌ Down":
                        st.markdown(f'<div class="card-guide">Run: <code>{restart_command}</code></div>', unsafe_allow_html=True)

                    st.markdown(f'</div>', unsafe_allow_html=True) # End status container


                    # End card wrapper
                    st.markdown(f'</div>', unsafe_allow_html=True)