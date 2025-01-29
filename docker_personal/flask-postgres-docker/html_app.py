from flask import Flask,render_template, request,jsonify,redirect,url_for
import psycopg2
from psycopg2 import sql
import os
app=Flask(__name__)


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
    
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        
        #INSERT THE DATA INTO THE 'people' table in 'de_docker' schema
        try:  

            conn = get_db_connection()
            
            cur = conn.cursor()
            cur.execute("SHOW search_path;")
            print("ok")
            print(cur.fetchone())
            cur.execute("SELECT current_database(), current_schema();")
            print(cur.fetchone())
            
            # Log the query
            query = 'INSERT INTO "people" (name, created_at) VALUES (%s, NOW())'
            print(f"Executing query: {query} with values: {name}")
            cur.execute(
                'INSERT INTO de_docker.people (name, created_at) VALUES (%s, NOW())',(name,)
            )
            conn.commit()
            
            cur.close()
            conn.close()
            print("data  inserted successfully")
          
        except Exception as e:
             print(f"error occured: {e}")
             return f"Error :  {e}"


        return redirect(url_for('index'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')