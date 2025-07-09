import json
import pandas as pd
from pandas import json_normalize
import psycopg2
from psycopg2.extras import execute_values
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Database connection details
DB_NAME = "sufyan"
DB_USER = "postgres"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    # Load and flatten JSON
    logging.info("Loading JSON data from dummy_data.json")
    with open('dummy_data.json') as f:
        data = json.load(f)

    logging.info("Flattening JSON data")
    df = json_normalize(data)

    # Convert orders column to JSON strings
    df['orders'] = df['orders'].apply(json.dumps)

    # Prepare data as a list of tuples
    records = df.to_records(index=False).tolist()

    # Connect to PostgreSQL
    logging.info("Connecting to PostgreSQL database")
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # Bulk insert without mapping each column
    query = """
        INSERT INTO dummy_data (id, name, email, orders, street, city, zipcode)
        VALUES %s
    """
    execute_values(cursor, query, records)

    # Commit changes
    conn.commit()
    logging.info("✅ JSON data bulk imported into PostgreSQL table dummy_data")

except Exception as e:
    logging.error(f"❌ An error occurred: {e}")
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
        logging.info("🔒 Database connection closed")
