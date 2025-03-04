import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import plotly.express as px

# Database connection details
DB_HOST = "localhost"  # e.g., "localhost" or an IP
DB_PORT = "5432"       # Default PostgreSQL port
DB_NAME = "de_personal"
DB_USER = "postgres"
DB_PASS = "animesh11"


# Create database engine
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

st.title("📊 PostgreSQL Database")

# Fetch schemas

def get_schemas():
    query = "SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('pg_catalog', 'information_schema');"
    return pd.read_sql(query, engine)["schema_name"].tolist()

# Fetch tables based on schema

def get_tables(schema):
    query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}';"
    return pd.read_sql(query, engine)["table_name"].tolist()

# Fetch table data

def load_data(schema, table):
    query = f'SELECT * FROM "{schema}"."{table}" LIMIT 100;'  # Fetch first 100 rows
    return pd.read_sql(query, engine)


# Truncate table
def truncate_table(schema, table,custom_query=None):
    try:
        with engine.connect() as connection:
            # If custom_query is provided, use it, otherwise generate default query
            query = custom_query or f'TRUNCATE TABLE "{schema}"."{table}";'
            query = text(query)
            connection.execute(query)
            connection.commit()
            st.success(f"✅ Table `{schema}.{table}` has been truncated successfully.")
    except Exception as e:
        st.error(f"❌ Error truncating table `{schema}.{table}`: {e}")


def drop_table(schema, table,query):
    try:
        with engine.connect() as connection:
            # If custom_query is provided, use it, otherwise generate default query

            query = text(query)
            connection.execute(query)
            connection.commit()

            st.success(f"✅ Table `{schema}.{table}` has been DROPPED successfully.")
    except Exception as e:
        st.error(f"❌ Error DROPING table `{schema}.{table}`: {e}")

# Schema selection
schemas = get_schemas()
selected_schema = st.sidebar.selectbox("🗂 Select Schema", schemas)

# Table selection
if selected_schema:
    tables = get_tables(selected_schema)
    selected_table = st.sidebar.selectbox("📋 Select Table", tables)

    # Fetch button to reload data
    if st.button("🔄 Fetch Data"):
        if selected_table:
            data = load_data(selected_schema, selected_table)
            st.write(f"### 📜 Data from `{selected_schema}.{selected_table}`")
            st.dataframe(data)

            # Download button
            csv = data.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV", data=csv, file_name=f"{selected_table}.csv", mime="text/csv")
            # ✅ Check if recorded_at exists and convert to datetime
            if 'recorded_at' in data.columns:
                data['recorded_at'] = pd.to_datetime(data['recorded_at'])

                # 📈 Line Chart: Visualizing Current Speed Over Time
                st.write("### 📊 Traffic Speed Over Time")
                fig = px.line(data, x="recorded_at", y="current_speed", title="Current Speed Over Time")
                st.plotly_chart(fig)

                # 📊 Bar Chart: Comparing Road Speeds
                st.write("### 📊 Average Speed per Road")
                avg_speed = data.groupby("road_id")["current_speed"].mean().reset_index()
                fig2 = px.bar(avg_speed, x="road_id", y="current_speed", title="Average Speed per Road",
                              labels={"road_id": "Road ID", "current_speed": "Avg Speed"})
                st.plotly_chart(fig2)

        else:
            st.warning("Please select a table to fetch data.")
        # Display and allow editing the query

    truncate_default_query = f'TRUNCATE TABLE "{selected_schema}"."{selected_table}"CASCADE;'
    drop_default_query = f'DROP TABLE IF EXISTS"{selected_schema}"."{selected_table}" CASCADE;'

    # Checkbox for editing queries
    if st.checkbox("Edit truncate query"):
        truncate_query = st.text_area("✏️ Edit Truncate Query", truncate_default_query, height=150)
    else:
        truncate_query = truncate_default_query  # Use default if checkbox is not checked

        # Truncate button to clear table data
    if st.button(f"🗑️ Truncate Table `{selected_schema}.{selected_table}`"):
            truncate_table(selected_schema, selected_table, truncate_query)

    if st.checkbox("Edit drop query"):
        drop_query = st.text_area("✏️ Edit DROP Query", drop_default_query, height=150)
    else:
        drop_query = drop_default_query  # Use default if checkbox is not checked

    # Drop button to remove table
    if st.button(f"🗑️ DROP Table `{selected_schema}.{selected_table}`"):
            drop_table(selected_schema, selected_table, drop_query)

        # New feature: Custom Query Execution
    st.subheader("🔍 Custom SQL Query Editor")
    custom_query = st.text_area("Enter your SQL query here:", height=200)

    if st.button("Execute Query"):
        if custom_query:
            try:
                # Execute the custom query
                result = pd.read_sql(custom_query, engine)
                st.write("### Query Result")
                st.dataframe(result)

                # Optionally, provide a download button
                csv = result.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Download CSV", data=csv, file_name="query_result.csv", mime="text/csv")
            except Exception as e:
                st.error(f"❌ Error executing query: {e}")
        else:
            st.warning("Please enter a SQL query.")



