'''from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient("mongodb+srv://sufyanmalik:QsjfIC74yTxCgrXH@cluster0.8awuxv8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0 is this my URL")  # or your MongoDB Atlas URL
db = client["test_db"]  # Create or connect to DB
collection = db["test_collection"]  # Create or connect to collection

# Load JSON data from file
with open("sample_data.json") as file:
    data = json.load(file)

# Insert data into MongoDB
insert_result = collection.insert_many(data)

print(f"✅ Inserted {len(insert_result.inserted_ids)} documents into MongoDB.")
'''

import pymongo
from datetime import datetime

# MongoDB connection
MONGO_URI = "mongodb+srv://sufyanmalik:QsjfIC74yTxCgrXH@cluster0.8awuxv8.mongodb.net"
DATABASE_NAME = "test_db"
COLLECTION_NAME = "test_collection"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]



# --- 2️⃣ INSERT Bilal Haider (id=4) ---
new_document = {
    "_id": 4,
    "name": "Bilal Haider",
    "email": "bilal@example.com",
    "age": 35,
    "address": {
        "street": "111 Park St",
        "city": "Lahore",
        "zip": "54000"
    },
    "last_updated": datetime.utcnow()  # new timestamp
}

try:
    collection.insert_one(new_document)
    print("✅ Bilal Haider inserted.")
except pymongo.errors.DuplicateKeyError:
    print("⚠️ Bilal Haider already exists.")

# Close connection
client.close()


'''
import pymongo
import snowflake.connector
from pprint import pprint

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
SNOWFLAKE_DATABASE = "ETL_DB"
SNOWFLAKE_SCHEMA = "PUBLIC"
SNOWFLAKE_TABLE = "SUFYAN"

# --- CONNECT TO MONGODB ---
mongo_client = pymongo.MongoClient(MONGO_URI)
mongo_db = mongo_client[DATABASE_NAME]
collection = mongo_db[COLLECTION_NAME]

# Fetch all records
mongo_data = list(collection.find())
print(f"✅ Found {len(mongo_data)} records in MongoDB.")

# Print MongoDB records
for doc in mongo_data:
    pprint(doc)

# --- CONNECT TO SNOWFLAKE ---
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

# --- CREATE TABLE ---
create_table_query = f"""
CREATE OR REPLACE TABLE "{SNOWFLAKE_TABLE}" (
    "_id" STRING,
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
print(f"✅ Table '{SNOWFLAKE_TABLE}' created in Snowflake.")


# --- INSERT DATA ---
for doc in mongo_data:
    _id = str(doc.get('_id'))
    name = doc.get('name', '')
    email = doc.get('email', '')
    age = doc.get('age', 0)
    address = doc.get('address', {})
    street = address.get('street', '')
    city = address.get('city', '')
    zip_code = address.get('zip', '')
    last_updated = doc.get('last_updated', None)

    insert_query = f"""
    INSERT INTO "{SNOWFLAKE_TABLE}" ("_id", "name", "email", "age", "street", "city", "zip", "last_updated")
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    sf_cursor.execute(insert_query, (
        _id, name, email, age, street, city, zip_code, last_updated
    ))
    print(f"📤 Inserted record {_id} into Snowflake.")
    
# --- CLEANUP ---
sf_connection.commit()
sf_cursor.close()
sf_connection.close()
mongo_client.close()
print("✅ All data successfully migrated to Snowflake.")
'''