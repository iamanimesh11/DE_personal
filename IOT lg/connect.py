import psycopg2

def check_postgres_connection(connection_params):
    try:
        conn = psycopg2.connect(**connection_params)  # Use keyword arguments
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # Simple test query
        result = cursor.fetchone()
        if result[0] != 1:
            print("Warning: Test query failed. Connection might be good, but database may have issues.")

        print("Successfully connected to PostgreSQL database.")
        conn.close()
        return True

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return False

# Example usage:
postgres_params = {
    "host": "localhost",
    "database": "de_personal",
    "user": "airflow_user",
    "password": "animesh11"
}

if check_postgres_connection(postgres_params):
    print("PostgreSQL connection OK")
else:
    print("PostgreSQL connection failed")