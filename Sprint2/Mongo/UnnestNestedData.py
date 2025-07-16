#in this file we are unnesting the nested data from mongodb to snowflake

import pymongo
import snowflake.connector

# --- MONGO DB CONNECTION ---
MONGO_URI = "mongodb+srv://sufyanmalik:QsjfIC74yTxCgrXH@cluster0.8awuxv8.mongodb.net"
DATABASE_NAME = "test_db"
COLLECTION_NAME = "test_collection"

# Connect to MongoDB
mongo_client = pymongo.MongoClient(MONGO_URI)
mongo_db = mongo_client[DATABASE_NAME]
collection = mongo_db[COLLECTION_NAME]

# Fetch all documents
mongo_data = list(collection.find())
print(f"✅ Fetched {len(mongo_data)} documents from MongoDB.")

# Flatten nested data
flattened_data = []
for doc in mongo_data:
    base = {
        "id": str(doc.get('_id')),
        "name": doc.get('name', ''),
        "age": doc.get('age', 0),
        "street": doc.get('address', {}).get('street', ''),
        "city": doc.get('address', {}).get('city', ''),
        "zip": doc.get('address', {}).get('zip', '')
    }
    orders = doc.get('orders', [])
    for order in orders:
        flat_doc = base.copy()
        flat_doc["order_id"] = order.get('order_id', '')
        flat_doc["amount"] = order.get('amount', 0)
        flat_doc["items"] = ", ".join(order.get('items', []))  # Join list into string
        flattened_data.append(flat_doc)

print(f"✅ Flattened into {len(flattened_data)} rows.")

# --- SNOWFLAKE CONNECTION ---
SNOWFLAKE_ACCOUNT = "pgdgtoc-ee29791"
SNOWFLAKE_USER = "sufyan"
SNOWFLAKE_PASSWORD = "xTwfVyLpGK44TDF"
SNOWFLAKE_WAREHOUSE = "etl_warehouse"
SNOWFLAKE_DATABASE = "etl_db"
SNOWFLAKE_SCHEMA = "PUBLIC"
SNOWFLAKE_ROLE = "ACCOUNTADMIN"
SNOWFLAKE_TABLE = "mongo_flat_data"

# Connect to Snowflake
sf_connection = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
    role=SNOWFLAKE_ROLE
)

sf_cursor = sf_connection.cursor()
print("✅ Connected to Snowflake.")

# --- CREATE TABLE IF NOT EXISTS ---
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {SNOWFLAKE_TABLE} (
    id STRING,
    name STRING,
    age INT,
    street STRING,
    city STRING,
    zip STRING,
    order_id STRING,
    amount FLOAT,
    items STRING
);
"""
sf_cursor.execute(create_table_query)
print(f"✅ Ensured table {SNOWFLAKE_TABLE} exists.")

# --- INSERT DATA INTO SNOWFLAKE ---
for row in flattened_data:
    insert_query = f"""
    INSERT INTO {SNOWFLAKE_TABLE} (id, name, age, street, city, zip, order_id, amount, items)
    VALUES (%(id)s, %(name)s, %(age)s, %(street)s, %(city)s, %(zip)s, %(order_id)s, %(amount)s, %(items)s)
    """
    sf_cursor.execute(insert_query, row)

print(f"✅ Loaded {len(flattened_data)} rows into Snowflake table '{SNOWFLAKE_TABLE}'.")

# Close connections
sf_cursor.close()
sf_connection.close()
mongo_client.close()
print("✅ All connections closed.")
