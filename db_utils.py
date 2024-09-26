import psycopg2
import os

# Fetch PostgreSQL connection settings from environment variables
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')  # Or 'postgres' if using Docker compose
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

def get_db_connection():
    try:
        # Establish the PostgreSQL connection
        conn = psycopg2.connect(
            dbname=POSTGRES_DB, 
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD, 
            host=POSTGRES_HOST, 
            port=POSTGRES_PORT
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to the PostgreSQL database: {e}")
        return None
