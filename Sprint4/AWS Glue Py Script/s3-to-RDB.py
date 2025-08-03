
#Step 1: Test Glue connection & list all databases
'''
import boto3

REGION = "eu-north-1"

print("🔍 Connecting to Glue...")
glue_client = boto3.client("glue", region_name=REGION)

print("📂 Listing Glue Databases...")
databases = glue_client.get_databases()

for db in databases["DatabaseList"]:
    print(f" - {db['Name']}")
'''

#Step 2: List tables inside your Glue database
'''
import boto3

REGION = "eu-north-1"
CATALOG_DATABASE = " pgdatabase-1"  # replace if different

print(f"🔍 Listing tables in Glue DB: {CATALOG_DATABASE}")
glue_client = boto3.client("glue", region_name=REGION)

tables = glue_client.get_tables(DatabaseName=CATALOG_DATABASE)

for t in tables["TableList"]:
    print(f" - {t['Name']}")
'''
#Step 3: Get table location (S3 path)
'''
import boto3

REGION = "eu-north-1"
CATALOG_DATABASE = " pgdatabase-1"
CATALOG_TABLE = "customers"

glue_client = boto3.client("glue", region_name=REGION)

print(f"🔍 Getting location of table {CATALOG_TABLE}...")
response = glue_client.get_table(DatabaseName=CATALOG_DATABASE, Name=CATALOG_TABLE)

s3_path = response["Table"]["StorageDescriptor"]["Location"]
print(f"📦 S3 Path: {s3_path}")
'''
#Step 4: Download S3 file
'''
import boto3
import tempfile

REGION = "eu-north-1"
s3_path = "s3://sufyan-ki-bucket/rawData/customers/customers.csv"  # replace from Step 3

s3_client = boto3.client("s3", region_name=REGION)

bucket_name = s3_path.replace("s3://", "").split("/", 1)[0]
object_key = s3_path.replace("s3://", "").split("/", 1)[1]

print(f"📥 Downloading {object_key} from {bucket_name}...")

temp_file = tempfile.NamedTemporaryFile(delete=False)
s3_client.download_file(bucket_name, object_key, temp_file.name)

print(f"✅ Downloaded to {temp_file.name}")
'''
#Step 5: Test connection to RDS PostgreSQL
'''
import psycopg2

# ======== CONFIG =========
DB_HOST = "postgres.clwcyeea822i.eu-north-1.rds.amazonaws.com"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASSWORD = "Paki$tani123$$$"
DB_NAME = "postgres"  # <-- You might need to change this! See note below
# =========================

try:
    print("🔗 Connecting to RDS PostgreSQL...")
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print("✅ Connected successfully!")

    # Check PostgreSQL version
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"🛠️ PostgreSQL version: {version[0]}")

    cur.close()
    conn.close()
    print("🔌 Connection closed.")

except Exception as e:
    print("❌ Connection failed!")
    print(e)
'''
#Step 6: Create Target Table in RDS
'''
import psycopg2

# ======== CONFIG =========
DB_HOST = "postgres.clwcyeea822i.eu-north-1.rds.amazonaws.com"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASSWORD = "Paki$tani123$$$"
DB_NAME = "postgres"  # <-- Use the correct DB name here (not instance ID!)
# =========================

TARGET_TABLE = "DestinationTable"

try:
    print("🔗 Connecting to RDS...")
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    print("✅ Connected to RDS.")

    # Create table if not exists
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {TARGET_TABLE} (
        id INT,
        name TEXT,
        age INT
    );
    """
    cur.execute(create_table_sql)
    conn.commit()

    print(f"🛠️ Table `{TARGET_TABLE}` is ready in RDS.")

    cur.close()
    conn.close()
    print("🔌 Connection closed.")

except Exception as e:
    print("❌ Failed to create table in RDS.")
    print(e)
'''

'''
import csv
import psycopg2

# ======== CONFIG =========
DB_HOST = "postgres.clwcyeea822i.eu-north-1.rds.amazonaws.com"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASSWORD = "Paki$tani123$$$"
DB_NAME = "postgres"
TARGET_TABLE = "DestinationTable"

temp_file_path = "/tmp/tmp6tva1zpb"  # Change if needed
# =========================

try:
    print("🔗 Connecting to RDS...")
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    print("✅ Connected to RDS.")

    with open(temp_file_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header if exists

        sql = f"""
        INSERT INTO {TARGET_TABLE} (id, first_name, last_name, full_name)
        VALUES (%s, %s, %s, %s)
        """

        rows_inserted = 0
        for row in reader:
            if len(row) < 4:
                print(f"⚠️ Skipping incomplete row: {row}")
                continue
            cur.execute(sql, tuple(row[:4]))
            rows_inserted += 1


    conn.commit()
    cur.close()
    conn.close()

    print(f"🎉 Successfully inserted {rows_inserted} rows into `{TARGET_TABLE}`.")

except Exception as e:
    print("❌ Failed to insert CSV data into RDS.")
    print(e)
'''
#Step 7: Insert CSV Data into RDS

import psycopg2

# ======== CONFIG =========
DB_HOST = "postgres.clwcyeea822i.eu-north-1.rds.amazonaws.com"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASSWORD = "Paki$tani123$$$"
DB_NAME = "postgres"
TARGET_TABLE = "DestinationTable"
# =========================

try:
    print("🔗 Connecting to RDS...")
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    print("✅ Connected to RDS.")

    # Query first 10 rows
    cur.execute(f"SELECT * FROM {TARGET_TABLE} LIMIT 10;")
    rows = cur.fetchall()

    # Print column names
    colnames = [desc[0] for desc in cur.description]
    print("📋 Columns:", colnames)

    # Print each row
    for row in rows:
        print(row)

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Failed to fetch data.")
    print(e)
