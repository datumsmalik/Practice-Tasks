import psycopg2
import csv
import json

# Database connection details
DB_NAME = "sufyan"
DB_USER = "postgres"          # Change if needed
DB_PASSWORD = "pakistan" # Replace with your password
DB_HOST = "localhost"
DB_PORT = "5432"

# Path to your CSV file
CSV_FILE_PATH = "/home/user5/Desktop/Practice/Day3/dummy_data.csv"

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("✅ Connected to database")

    # Open the CSV file
    with open(CSV_FILE_PATH, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row

        for row in reader:
            # Fix the JSON formatting in the 'orders' column
            try:
                orders_json = json.dumps(eval(row[3]))  # Safely convert string to JSON
            except Exception as json_err:
                print(f"⚠️ Skipping row due to JSON error: {json_err}")
                continue

            # Insert each row into the table
            cursor.execute("""
                INSERT INTO dummy_data (id, name, email, orders, street, city, zipcode)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (row[0], row[1], row[2], orders_json, row[4], row[5], row[6]))

    # Commit changes
    conn.commit()
    print("✅ CSV data imported successfully!")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("🔒 Database connection closed")
