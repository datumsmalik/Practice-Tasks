#in this task we load data from postgress same table we created in preious task and load it   to snowflake


import dlt 

#SOURCE DEFINE KRTE HAIN

@dlt.source 
def src():
    # replace karega existing table in snowflake with new data
    # append karega new data to existing table in snowflake

    
    @dlt.resource(write_disposition="replace")  #resource matlab ye btae ga DLT ko btata he traet it as a table in destination
    def load_testing_table():
        import psycopg2

        creds = dlt.secrets["postgres.credentials"] # header ka name he 

        
        if creds is None:
            raise ValueError("Postgres credentials not found")
        
        print("connecting to postgres")

        conn=psycopg2.connect(
            host=creds["host"],
            port=creds["port"],
            database=creds["database"],
            user=creds["username"],
            password=creds["password"]
        )

        cur=conn.cursor() # cursor SQL queries ko execute karega postgres me 

        cur.execute("SET search_path TO public;") # ye schema he 

        cur.execute("SELECT * FROM testing")

        columns=[desc[0] for desc in cur.description]  # cur.description contains is list of tuples each tuple contain information about 1 column 
        
        rows=cur.fetchall() # ye rows ko fetch karega postgres me se 

        cur.close() 
        conn.close() # ye connection close karega postgres me se 

        print(f"Itni ({len(rows)}) rows ko load krne k liye mubarak ho")

        #ye rows ko dictionary me convert krte hain for dlt
        for row in rows:
            yield dict(zip(columns, row)) # rows or columns ko zip karega and dictionary me convert karega 

#acha to yield sari rows ko 1 dafa bhegne ki bijae  yield send one dictionery at a time 
# ye is lie kia he kyun k ham function ko as a generator use krte he jo data row by row send karega 

    return load_testing_table()
    

#ab pipline create krte hain
pipeline=dlt.pipeline(
    pipeline_name="postgres_to_snowflake",
    destination="snowflake",
    dataset_name="public"
)

load_info=pipeline.run(src())
print(f"{load_info.loads_ids}data load ho gaya hurray")
        
