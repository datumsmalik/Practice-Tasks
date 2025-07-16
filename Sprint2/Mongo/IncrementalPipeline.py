#in this file we are using incremental pipeline to load data from mongodb to snowflake

import pymongo
import snowflake.connector
from datetime import datetime
import os

# --- CONFIGURATION ---

# MongoDB connection
MONGO_URI = "mongodb+srv://sufyanmalik:QsjfIC74yTxCgrXH@cluster0.8awuxv8.mongodb.net"
DATABASE_NAME = "test_db"
COLLECTION_NAME = "test_collection"

# Snowflake connection
SNOWFLAKE_ACCOUNT = "pgdgtoc-ee29791"
SNOWFLAKE_USER = "sufyan"
SNOWFLAKE_PASSWORD = "xTwfVyLpGK44TDF"
SNOWFLAKE_WAREHOUSE = "etl_warehouse"
SNOWFLAKE_DATABASE = "etl_db"
SNOWFLAKE_SCHEMA = "PUBLIC"
SNOWFLAKE_TABLE = "SUFYAN"

# Incremental tracking file
LAST_SYNC_FILE = "last_sync.txt"

# --- FUNCTIONS ---

def get_last_sync():
    """Retrieve last sync timestamp or default to epoch start"""
    if os.path.exists(LAST_SYNC_FILE):
        with open(LAST_SYNC_FILE, "r") as f:
            return datetime.fromisoformat(f.read().strip())
    else:
        print("⚠️ No last_sync.txt found. Running full load.")
        return datetime.fromisoformat("1970-01-01T00:00:00")

def update_last_sync(timestamp):
    """Save latest sync timestamp"""
    with open(LAST_SYNC_FILE, "w") as f:
        f.write(timestamp.isoformat())

# --- MONGO DB CONNECTION ---
mongo_client = pymongo.MongoClient(MONGO_URI)
mongo_db = mongo_client[DATABASE_NAME]
collection = mongo_db[COLLECTION_NAME]

# --- FETCH ONLY NEW/UPDATED RECORDS ---
last_sync_time = get_last_sync()
print(f"🔄 Fetching records updated after {last_sync_time}...")

query = {"last_updated": {"$gt": last_sync_time}}
mongo_data = list(collection.find(query))
print(f"✅ Found {len(mongo_data)} new/updated records in MongoDB.")

if mongo_data:
    for doc in mongo_data:
        print("\n📥 New/Updated record:")
        print(doc)
else:
    print("⚠️ No new/updated records found.")

# --- SNOWFLAKE CONNECTION ---
sf_connection = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA
)
sf_cursor = sf_connection.cursor()
print("✅ Connected to Snowflake.")

# --- ENSURE TABLE EXISTS ---
create_table_query = f"""
CREATE TABLE IF NOT EXISTS "{SNOWFLAKE_TABLE}" (
    "_id" STRING PRIMARY KEY,
    "name" STRING,
    "email" STRING,
    "age" NUMBER,
    "street" STRING,
    "city" STRING,
    "zip" STRING,
    "last_updated" TIMESTAMP_NTZ
);
"""
sf_cursor.execute(create_table_query)
print(f"✅ Table '{SNOWFLAKE_TABLE}' is ready in Snowflake.")

# --- INSERT OR UPDATE DATA ---
for doc in mongo_data:
    _id = str(doc.get('_id'))
    name = doc.get('name', '')
    email = doc.get('email', '')
    age = doc.get('age', 0)
    address = doc.get('address', {})
    street = address.get('street', '')
    city = address.get('city', '')
    zip_code = address.get('zip', '')
    last_updated = doc.get('last_updated')

    # Upsert into Snowflake
    merge_query = f"""
MERGE INTO "{SNOWFLAKE_TABLE}" AS target
USING (SELECT %s AS _id) AS source
ON target."_id" = source._id
WHEN MATCHED THEN UPDATE SET
    "name"=%s, "email"=%s, "age"=%s,
    "street"=%s, "city"=%s, "zip"=%s, "last_updated"=%s
WHEN NOT MATCHED THEN INSERT ("_id", "name", "email", "age", "street", "city", "zip", "last_updated")
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""

    params = (
        _id, name, email, age, street, city, zip_code, last_updated,
        _id, name, email, age, street, city, zip_code, last_updated
    )
    print(f"📤 Executing MERGE for record {_id}...")
    sf_cursor.execute(merge_query, params)

print(f"✅ Loaded {len(mongo_data)} new/updated records into Snowflake table '{SNOWFLAKE_TABLE}'.")

# Update last sync timestamp
if mongo_data:
    latest_timestamp = max(doc["last_updated"] for doc in mongo_data)
    update_last_sync(latest_timestamp)
    print(f"✅ Updated last sync timestamp to {latest_timestamp}.")

# --- CLEANUP ---
sf_cursor.close()
sf_connection.close()
mongo_client.close()
print("✅ All connections closed.")
