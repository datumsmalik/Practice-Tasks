#in this file we are testing and validating the pipeline

import pymongo
import snowflake.connector

# --- MongoDB Connection ---
MONGO_URI = "mongodb+srv://sufyanmalik:QsjfIC74yTxCgrXH@cluster0.8awuxv8.mongodb.net"
DATABASE_NAME = "test_db"
COLLECTION_NAME = "test_collection"

mongo_client = pymongo.MongoClient(MONGO_URI)
mongo_db = mongo_client[DATABASE_NAME]
collection = mongo_db[COLLECTION_NAME]

# Get MongoDB row count
mongo_count = collection.count_documents({})
print(f"✅ MongoDB row count: {mongo_count}")

# --- Snowflake Connection ---
sf_connection = snowflake.connector.connect(
    user="sufyan",
    password="xTwfVyLpGK44TDF",
    account="pgdgtoc-ee29791",
    warehouse="etl_warehouse",
    database="etl_db",
    schema="PUBLIC",
    role="ACCOUNTADMIN"
)
sf_cursor = sf_connection.cursor()

# Get Snowflake row count
sf_cursor.execute("SELECT COUNT(*) FROM mongo_data")
sf_count = sf_cursor.fetchone()[0]
print(f"✅ Snowflake row count: {sf_count}")

# --- Validation ---
if mongo_count == sf_count:
    print("🎉 SUCCESS: Row counts match!")
else:
    print("❌ ERROR: Row counts do NOT match!")

# Close connections
sf_cursor.close()
sf_connection.close()
mongo_client.close()
print("✅ Connections closed.")
