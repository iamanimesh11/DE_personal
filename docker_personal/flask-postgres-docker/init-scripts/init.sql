-- Step 1: Create database if it doesn't exist (Only works when running outside the DB)
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'de_database') THEN
        CREATE DATABASE de_database;
    END IF;
END $$;

-- Connect to the new database (Docker’s init.sql runs inside the container, so this part may be skipped)
\c de_database;

-- Step 2: Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS de_docker;

-- Step 3: Create table if it doesn't exist
CREATE TABLE IF NOT EXISTS 
de_docker.people (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INTEGER ,
    created_at TIMESTAMP DEFAULT NOW()
);
