import psycopg2

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'postgres'
POSTGRES_DB = 'postgres'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'

def get_db_connection():
    conn = psycopg2.connect(
        dbname=POSTGRES_DB, user=POSTGRES_USER,
        password=POSTGRES_PASSWORD, host=POSTGRES_HOST, port=POSTGRES_PORT
    )
    return conn