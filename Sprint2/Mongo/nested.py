import pymongo

# MongoDB connection
MONGO_URI = "mongodb+srv://sufyanmalik:QsjfIC74yTxCgrXH@cluster0.8awuxv8.mongodb.net"
DATABASE_NAME = "test_db"
COLLECTION_NAME = "test_collection"

# Connect to MongoDB    
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Nested JSON documents
nested_documents = [
    {
        "name": "Alice",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "Karachi",
            "zip": "74000"
        },
        "orders": [
            {"order_id": "A001", "amount": 250, "items": ["apple", "banana"]},
            {"order_id": "A002", "amount": 150, "items": ["grapes"]}
        ]
    },
    {
        "name": "Bob",
        "age": 25,
        "address": {
            "street": "456 Park Ave",
            "city": "Lahore",
            "zip": "54000"
        },
        "orders": [
            {"order_id": "B001", "amount": 500, "items": ["mango", "pear"]},
            {"order_id": "B002", "amount": 300, "items": ["peach"]}
        ]
    }
]

# Insert nested documents into MongoDB
insert_result = collection.insert_many(nested_documents)
print(f"✅ Inserted {len(insert_result.inserted_ids)} nested documents into MongoDB.")
