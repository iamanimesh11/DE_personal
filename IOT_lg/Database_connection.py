import psycopg2
# Connect to DB
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
db_config = config['database']
host = db_config['host']
username = db_config['user']
password = db_config['password']
port = db_config['port']
database_name = db_config['database']


def connect_Database():
    try:
        conn = psycopg2.connect(
            dbname=database_name,
            user=username,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # Simple test query
        result = cursor.fetchone()
        if result[0] != 1:
            print("Warning: Test query failed. Connection might be good, but database may have issues.")

        print("Successfully connected to PostgreSQL database.")
        conn.close()
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")  # Indicate failure with error message
        return None  # Return None to signal failure
