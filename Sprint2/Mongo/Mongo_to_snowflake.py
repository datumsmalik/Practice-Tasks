#in this file we are using dlt to load data from mongodb to snowflake 

'''import pymongo
import snowflake.connector

# --- MONGO DB CONNECTION ---
MONGO_URI = "mongodb+srv://sufyanmalik:QsjfIC74yTxCgrXH@cluster0.8awuxv8.mongodb.net"
DATABASE_NAME = "test_db"        # Replace with your DB name
COLLECTION_NAME = "test_collection"  # Replace with your collection name

# Connect to MongoDB
mongo_client = pymongo.MongoClient(MONGO_URI)
mongo_db = mongo_client[DATABASE_NAME]
collection = mongo_db[COLLECTION_NAME]

# Fetch all documents
mongo_data = list(collection.find())

print(f"✅ Fetched {len(mongo_data)} documents from MongoDB.")

# --- SNOWFLAKE CONNECTION ---
SNOWFLAKE_ACCOUNT = "pgdgtoc-ee29791"
SNOWFLAKE_USER = "sufyan"
SNOWFLAKE_PASSWORD = "xTwfVyLpGK44TDF"
SNOWFLAKE_WAREHOUSE = "etl_warehouse"
SNOWFLAKE_DATABASE = "etl_db"  # Fixed typo
SNOWFLAKE_SCHEMA = "PUBLIC"
SNOWFLAKE_ROLE = "ACCOUNTADMIN"
SNOWFLAKE_TABLE = "mongo_data"

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
    city STRING
);
"""
sf_cursor.execute(create_table_query)
print(f"✅ Ensured table {SNOWFLAKE_TABLE} exists.")

# --- INSERT DATA INTO SNOWFLAKE ---
for doc in mongo_data:
    doc_id = str(doc.get('_id'))
    name = doc.get('name', '')
    age = doc.get('age', 0)
    city = doc.get('city', '')

    insert_query = f"""
    INSERT INTO {SNOWFLAKE_TABLE} (id, name, age, city)
    VALUES (%(id)s, %(name)s, %(age)s, %(city)s)
    """
    sf_cursor.execute(insert_query, {
        "id": doc_id,
        "name": name,
        "age": age,
        "city": city
    })

print(f"✅ Loaded {len(mongo_data)} documents into Snowflake table '{SNOWFLAKE_TABLE}'.")

# Close connections
sf_cursor.close()
sf_connection.close()
mongo_client.close()
print("✅ All connections closed.")
'''


import dlt
import pymongo

# --- MONGODB CONNECTION ---
MONGO_URI = "mongodb+srv://sufyanmalik:QsjfIC74yTxCgrXH@cluster0.8awuxv8.mongodb.net"
DATABASE_NAME = "test_db"
COLLECTION_NAME = "test_collection"

def get_mongo_data():
    # Connect to MongoDB
    mongo_client = pymongo.MongoClient(MONGO_URI)
    mongo_db = mongo_client[DATABASE_NAME]
    collection = mongo_db[COLLECTION_NAME]

    # Yield each document
    for doc in collection.find():
        # Convert ObjectId to string for Snowflake compatibility
        doc["_id"] = str(doc["_id"])
        yield doc

    mongo_client.close()

# --- DLT RESOURCE ---
@dlt.source
def mongo_source():
    @dlt.resource(write_disposition="replace")  # Replace table contents each run
    def mongo_data():
        yield from get_mongo_data()
    return mongo_data

# --- DLT PIPELINE ---
pipeline = dlt.pipeline(
    pipeline_name="mongo_to_snowflake_pipeline",
    destination="snowflake",
    dataset_name="mongo_dataset"
)

# --- RUN PIPELINE ---
load_info = pipeline.run(
    mongo_source(),
    table_name="mongo_data"
)

print("✅ Data loaded into Snowflake!")
print(load_info)
