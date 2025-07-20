#now we take src as snow flake and destination as postgres using dlt



import dlt 
import snowflake.connector


#SOURCE DEFINE KRTE HAIN

@dlt.source 
def src():
    # replace karega existing table in snowflake with new data
    # append karega new data to existing table in snowflake

    
    @dlt.resource(write_disposition="replace")  #resource matlab ye btae ga DLT ko btata he traet it as a table in destination
    def load_testing_table_pg():
        
        creds = dlt.secrets["snowflake.credentials"] # header ka name he 

        
        if creds is None:
            raise ValueError("snow flake credentials not found")
        
        print("connecting to snow flake")

        conn=snowflake.connector.connect(
            user=creds["username"],
            password=creds["password"],
            warehouse=creds["warehouse"],
            database=creds["database"],
            schema=creds["schema"],
            role=creds["role"],
            account=creds["host"]

        )



        cur=conn.cursor() # cursor SQL queries ko execute karega snow flake me 

      #  cur.execute("SET search_path TO public;") # ye schema he          # postgrtes version

        cur.execute(f"USE SCHEMA {creds['database']}.{creds['schema']};")  # snowflake version


        cur.execute("SELECT * FROM load_testing_table")

        columns=[desc[0] for desc in cur.description]  # cur.description contains is list of tuples each tuple contain information about 1 column 
        
        rows=cur.fetchall() # ye rows ko fetch karega snow flake me se 

        cur.close() 
        conn.close() # ye connection close karega snow flake me se 

        print(f"Itni ({len(rows)}) rows ko load krne k liye mubarak ho")

        #ye rows ko dictionary me convert krte hain for dlt
        for row in rows:
            yield dict(zip(columns, row)) # rows or columns ko zip karega and dictionary me convert karega 

#acha to yield sari rows ko 1 dafa bhegne ki bijae  yield send one dictionery at a time 
# ye is lie kia he kyun k ham function ko as a generator use krte he jo data row by row send karega 

    return load_testing_table_pg()
    

#ab pipline create krte hain
pipeline=dlt.pipeline(
    pipeline_name="snowflake_to_postgres",
    destination="postgres",
    dataset_name="public" # ye schema he 
)

load_info=pipeline.run(src()) 
print(f"{load_info.loads_ids}data load ho gaya hurray")
        
