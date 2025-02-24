import streamlit as st
import pandas as pd
import datetime

# File to store data
DATA_FILE = "time_log.csv"

# Function to load existing data
def load_data():
    try:
        return pd.read_csv(DATA_FILE, parse_dates=["Date"])
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Activity", "Category", "Start Time", "End Time", "Duration (mins)"])


# Function to save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# UI Title
st.title("📊 Personal Time Tracker")

# Sidebar - Activity Logging Form
st.sidebar.header("📝 Log Your Activity")

# Input fields
activity = st.sidebar.text_input("Activity Name")
category = st.sidebar.selectbox("Category", ["Work", "Exercise", "Leisure", "Learning", "Other"])
date = st.sidebar.date_input("Date", datetime.date.today())
start_time = st.sidebar.time_input("Start Time", value=datetime.datetime.now().time())
end_time = st.sidebar.time_input("End Time", value=datetime.datetime.now().time())

# Log Activity Button
if st.sidebar.button("➕ Log Activity"):
    if activity:
        # Calculate duration
        start_dt = datetime.datetime.combine(date, start_time)
        end_dt = datetime.datetime.combine(date, end_time)
        duration = (end_dt - start_dt).seconds / 60  # Convert to minutes


        # Load and update data
        df = load_data()
        new_entry = pd.DataFrame([[date, activity, category, start_time, end_time, duration]], 
                         columns=df.columns)
                         
        df = pd.concat([df, new_entry], ignore_index=True)
        save_data(df)

        st.sidebar.success("✅ Activity Logged!")
    else:
        st.sidebar.error("⚠️ Please enter an activity name.")

# Load and display data
df = load_data()

# Date filter for viewing logs
st.subheader("📅 Logged Activities")
selected_date = st.date_input("📆 Filter by Date", datetime.date.today())
filtered_df = df[df["Date"] == pd.to_datetime(selected_date)]
st.dataframe(filtered_df)

# Summary statistics
st.subheader("📊 Time Spent by Category")
category_summary = df.groupby("Category")["Duration (mins)"].sum()
st.bar_chart(category_summary)
