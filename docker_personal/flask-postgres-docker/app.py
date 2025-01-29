import string
import time

from flask import Flask,render_template, request,jsonify,redirect,url_for
import psycopg2
from psycopg2 import sql
import os
app=Flask(__name__)
import random

# Database connection parameters
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'de_database')  # Your database name
DB_USER = os.getenv('DB_USER', 'de_user')  # Your username
DB_PASSWORD = os.getenv('DB_PASSWORD', 'animesh11')  # Your password


# Establish PostgreSQL connection
def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        dbname="de_database",
        user="de_user",
        password="animesh11"
    )
    print(f"connected to database {DB_NAME} on host : {DB_HOST}")
    # Set the search path to de_docker schema
    conn.autocommit = True  # Commit the search_path change immediately
    cur = conn.cursor()
    cur.execute('SET search_path TO de_docker, public;')
    cur.close()
    print(f"connected   to database {DB_NAME} on host : {DB_HOST}")

    return conn

random_String=''.join(random.choices(string.ascii_letters+string.digits,k=5))
print(random_String)


def inserting_Random_Data_into_db(name,age):
    name=random_String
    #INSERT THE DATA INTO PEOPLE TABLE

    try:
        conn = get_db_connection()
        cur=conn.cursor()
        cur.execute("SHOW search_path;")
        print(f" showing search path is:  {cur.fetchone()}")
        query='INSERT INTO de_docker.people (name,age,created_at) VALUES (%s,%s,NOW())'
        print(f"executing query : {query} with values : name - {name}, age- {age}")
        cur.execute(query,(name,age))
        conn.commit()
        cur.close()
        conn.close()
        print(f" Data Inserted successfully")

    except Exception as e:
        print(f"Error in connection and inserting {e}")
        return f"Error: {e}"

for i in range(1,50):
    random_String = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    random_number=random.choice(list(range(1,99)))
    inserting_Random_Data_into_db(random_String,random_number)
    time.sleep(10)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')