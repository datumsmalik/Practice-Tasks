# in this task we use historical data we create in previous task1 and then load in snow flake via ELT pipeline

import pandas as pd
import psycopg2
import snowflake.connector
import os
from dotenv import load_dotenv 

load_dotenv()

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

# step no :pehla , extract data from postgress
PG_CONN=psycopg2.connect(
    database=PG_DATABASE,
    user=PG_USERNAME,
    password=PG_PASSWORD,
    host=PG_HOST,
    port=PG_PORT
)

df_pg=pd.read_sql_query("SELECT * FROM DATUM",PG_CONN)
PG_CONN.close()
print(f"Itne rows postgress me hai {len(df_pg)}")  #f-string string insert var direclty in string

#step no : dusra , load data from snow flake
SNOWFLAKE_CONN=snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
)
SNOWFLAKE_CURSOR=SNOWFLAKE_CONN.cursor()

#create table now we use other table in snow flake
SNOWFLAKE_CURSOR.execute("""
    CREATE TABLE IF NOT EXISTS DATUM2(
    id INT Primary Key,
    name TEXT,
    email TEXT
    )
""")

#loop to insert data from data frame to snow flake
for _, row in df_pg.iterrows():  # _ skip row index , row gives data of each row, df_pg uper vala var he jis me data store he
    SNOWFLAKE_CURSOR.execute(
        "INSERT INTO DATUM2 (id, name, email) VALUES (%s, %s, %s) ",
        (row["id"], row["name"], row["email"])
    )
SNOWFLAKE_CONN.commit()     

SNOWFLAKE_CURSOR.close()
SNOWFLAKE_CONN.close()

print("Data snow flake me load ho gaya dusre table me Alhamdulillah")


