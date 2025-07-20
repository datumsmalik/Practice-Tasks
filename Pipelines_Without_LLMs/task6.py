#now we take src  as mongo db and destination as snow flake

import dlt
import pymongo
import snowflake.connector
import certifi


#source define krte hain

@dlt.source
def mongo_source(): 
    @dlt.resource(name="data", write_disposition="replace") #replace karega existing table in snowflake with new data 
    def Data(): # ye table ka name he snow flake me 
        creds=dlt.secrets["mongo_credentials"] #header ka name he 

        if creds is None:
            raise ValueError("mongo credentials not found")
        
        print("connecting to mongo")

        #connect to mongo db
        mongo_client = pymongo.MongoClient(
    creds["connection_string"]
)





        mongo_db = mongo_client[creds["database"]]
        collection = mongo_db[creds["collection"]]


# fetch  data from mongo db
        documents=collection.find()
        count = collection.count_documents({})  # ye docs jo mongo me hain unhain count kre ga
        print(f"fetched {count} documents from mongo db")


        #yeild documents one by one
        for doc in documents:
            yield doc

        mongo_client.close()

    return Data()


# pipeline define krte hain

pipeline=dlt.pipeline(
    pipeline_name="mongo_to_snowflake",
    destination="snowflake",
    dataset_name="public"
)

pipeline.drop() #pehle previous table k name se pipeline run ki thi use drop kia he 
load_info=pipeline.run(mongo_source())
print(f"{load_info.loads_ids}data load ho gaya hurray")




'''
#dlt is designed primarily for loading data into SQL-style warehouses and lakes (like Snowflake, BigQuery, Redshift, Postgres).
It doesn’t ship a MongoDB destination out of the box.

MongoDB as a source = ✅
MongoDB as a destination = ❌ (not yet)

'''