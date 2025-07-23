
#postgres to snow flake ELT pipeline (with .env) by creating sample data 


import psycopg2 # for connecting to postgres database
import pandas as pd  # to fetch and move data easily 
import snowflake.connector # for connecting to snow flake database
import os # for loading environment variables
import pandas as pd # to create dataframe

from dotenv import load_dotenv # for loading environment variables from .env file


load_dotenv() # load environment variables from .env file

#postgres credentials from .env file these are from documentation of postgres

PG_DATABASE=os.getenv("PG_DATABASE")
PG_USERNAME=os.getenv("PG_USERNAME")
PG_PASSWORD=os.getenv("PG_PASSWORD")
PG_HOST=os.getenv("PG_HOST")
PG_PORT=os.getenv("PG_PORT")

#snow flake credentials from .env file these are from documentation of snow flake
SNOWFLAKE_USER=os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD=os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT=os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE=os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE=os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA=os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_ROLE=os.getenv("SNOWFLAKE_ROLE")
# env k name same hone chahye env me bhi 


# step no : pehla

data={
    "id": [1,2,3,4,5],
    "name": ["John", "Jane", "Jim", "Jill", "Jack"],
    "email": ["john@example.com", "jane@example.com", "jim@example.com", "jill@example.com", "jack@example.com"]
}


df=pd.DataFrame(data) # data ko rows or columns me convert karega 


# now connect to postgres database 
pg_conn=psycopg2.connect(
    database=PG_DATABASE,
    user=PG_USERNAME,
    password=PG_PASSWORD,
    host=PG_HOST,
    port=PG_PORT
)

pg_cursor=pg_conn.cursor() # cursor SQL queries ko execute karega postgres me 

# table create karega postgres me data insert krne ke liye 
pg_cursor.execute("""
    CREATE TABLE IF NOT EXISTS DATUM(
    id INT Primary Key,
    name TEXT,
    email TEXT
    )
""")
pg_conn.commit() # commit is like save button in DB asan alfaz me

#ye loop har row ko insert karega postgres me dataframe se le kr
for _, row in df.iterrows(): # this loop iterate through every row and gives you index and row itself now we using _ itmean to ignore index
    pg_cursor.execute(   #insert row into table
        "INSERT INTO DATUM (id, name, email) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;", # if row exsist phir insert nahi kare ga 
        (row["id"], row["name"], row["email"])
    )
pg_conn.commit() # commit karega postgres me data insert ho jayegi 
print("Sample data postgress me insert ho gaya")


#step no : dusra , extract data from posrgress
query="SELECT * FROM DATUM"
df_pg=pd.read_sql_query(query,pg_conn) # save result As a dataframe

pg_cursor.close()
pg_conn.close() # close connection to postgres database

# step no : tisra , load data into snow flake
snowflake_conn=snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
)

snowflake_cursor=snowflake_conn.cursor()

# create table in snow flake
snowflake_cursor.execute("""
    CREATE TABLE IF NOT EXISTS DATUM(
    id INT Primary Key,
    name TEXT,
    email TEXT
    )
""")
for _, row in df_pg.iterrows():    
    snowflake_cursor.execute(
        "INSERT INTO DATUM (id, name, email) VALUES (%s, %s, %s) ", 
        
        # %s is a placeholder for the actual data you’re inserting.
        (row["id"], row["name"], row["email"])
    )
snowflake_conn.commit() # commit karega snow flake me table create ho jayegi 
snowflake_cursor.close()
snowflake_conn.close() # close connection to snow flake database

print("Data snow flake me load ho gaya")

