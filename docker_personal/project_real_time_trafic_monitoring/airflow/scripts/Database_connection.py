import os
import random
import time

from logging_and_monitoring.centralized_logging import setup_logger

import psycopg2
# Connect to DB
import configparser
# Ensure the correct path inside Docker
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "credentials", "config.ini")
log_path=os.path.join(BASE_DIR, "logging_and_monitoring", "database_connection.log")
# Debugging: Print path to check if it exists
print("Looking for config file at:", CONFIG_PATH)

# Load the config file
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# Ensure the file is loaded correctly
if not config.sections():
    raise FileNotFoundError(f"Config file not found or empty: {CONFIG_PATH}")

config = configparser.ConfigParser()
config.read(CONFIG_PATH)
db_config = config['database']
host = db_config['host']
username = db_config['user']
password = db_config['password']
port = db_config['port']
database_name = db_config['database']
schema_name = "roads_traffic"  # Specify the schema to check

logger = setup_logger("database_logging", "database_connection", "postgres", log_path)


def connect_Database():
    logger.info("Database connection started.", extra={"stage": "start"})

    conn = None
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
            logger.warning("Test query failed. Connection seems unstable.", extra={"stage": "start"})
            conn.close()
            return None
            # Create schema if it does not exist
        logger.info("Successfully connected to PostgreSQL database.", extra={"stage": "success"})

        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
        conn.commit()
        logger.info(f"Schema '{schema_name}' is ready.", extra={"stage": "schema_setup"})
        query = f"""
               CREATE TABLE IF NOT EXISTS {schema_name}.roads(
                    road_id SERIAL PRIMARY KEY, 
                    road_name VARCHAR(255) NOT NULL UNIQUE,
                    start_lat DECIMAL(10, 7) NOT NULL, 
                    start_lon DECIMAL(10, 7) NOT NULL, 
                    end_lat DECIMAL(10, 7) NOT NULL,  
                    end_lon DECIMAL(10, 7) NOT NULL,   
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
               """
        cursor.execute(query=query)
        conn.commit()
        logger.info(f"Table 'roads' is ready.", extra={"stage": "table_setup"})
        # Create index for roads table safely
        try:
            cursor.execute(f"""
                        DO $$ BEGIN
                            IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'roads_road_id_idx') THEN
                                CREATE INDEX roads_road_id_idx ON {schema_name}.roads(road_id);
                            END IF;
                        END $$;
                    """)
            conn.commit()
            logger.info("Index 'roads_road_id_idx' created successfully.", extra={"stage": "index_creation"})
        except Exception as e:
            conn.rollback()
            logger.warning(f"Skipping index creation for 'roads_road_id_idx': {e}", extra={"stage": "index_creation"})

        query = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.traffic_data (
            traffic_id SERIAL PRIMARY KEY,
            road_id INT REFERENCES {schema_name}.roads(road_id) ON DELETE CASCADE,
            road_name TEXT,
            latitude DECIMAL(10, 6),
            longitude DECIMAL(10, 6),
            current_speed INT,
            free_flow_speed INT,
            current_travel_time INT,
            free_flow_travel_time INT,
            road_closure BOOLEAN DEFAULT FALSE,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            mapurl TEXT,
            weather_conditions VARCHAR(50) ,
            temperature FLOAT,
            humidity FLOAT,
            traffic_condition VARCHAR(50),
            FOREIGN KEY (road_id) REFERENCES {schema_name}.roads(road_id)          
        );
        """
        cursor.execute(query=query)
        conn.commit()
        logger.info(f"Table 'traffic_data' is ready.", extra={"stage": "table_setup"})
        # Create index for traffic_data table safely
        try:
            cursor.execute(f"""
                        DO $$ 
                            BEGIN
                                IF NOT EXISTS (
                                    SELECT 1 FROM pg_indexes WHERE LOWER(indexname) = LOWER('traffic_Data_road_id_idx')
                                ) THEN
                                    CREATE INDEX traffic_Data_road_id_idx ON roads_traffic.traffic_data(road_id);
                                END IF;
                            END $$;

                    """)
            conn.commit()
            logger.info("Index 'traffic_Data_road_id_idx' created successfully.", extra={"stage": "index_creation"})
        except Exception as e:
            conn.rollback()
            logger.warning(f"Skipping index creation for 'traffic_Data_road_id_idx': {e}",
                           extra={"stage": "index_creation"})

        logger.info("Database setup completed successfully.", extra={"stage": "success"})

        ti=Kwargs['ti']
        ti.xcom_push(key="db_connection",value)
        return conn

    except psycopg2.Error as e:
        logger.critical(f"Database connection error: {e}", extra={"stage": "start"})
        if conn:
            conn.close()  # Ensure connection is closed if an error occurs

        return 