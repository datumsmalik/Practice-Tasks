# implemented RDS-to-RDS via AWS Glue both using py script and pyspark

'''
#Step 1: Connect to RDS and list tables (RDS postgress se sare table list kr rhe hain)
import psycopg2

# RDS connection details
rds_host = "#"
rds_port = "#"
rds_db = "#"
rds_user = "#"
rds_password = "#"

try:
    # Connect to PostgreSQL RDS
    conn = psycopg2.connect(
        host=rds_host,
        port=rds_port,
        database=rds_db,
        user=rds_user,
        password=rds_password
    )
    print("Connected to RDS PostgreSQL")

    cur = conn.cursor()

    # Fetch all table names
    cur.execute("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
        ORDER BY table_schema, table_name;
    """)

    tables = cur.fetchall()

    if tables:
        print(" Tables in your RDS PostgreSQL:")
        for schema, table in tables:
            print(f"{schema}.{table}")
    else:
        print("⚠ No user tables found.")

    cur.close()
    conn.close()

except Exception as e:
    print(" Error connecting to RDS:", e)
'''





'''
#Step 2 — Create Glue table metadata from RDS data (idher sirf catalog DB create kr rhe hain)
import boto3

region_name = "#"

# Create Glue client
glue = boto3.client("glue", region_name=region_name)

database_name = "#"

try:
    glue.create_database(
        DatabaseInput={
            "Name": database_name,
            "Description": "Catalog for RDS PostgreSQL tables"
        }
    )
    print(f" Glue database '{database_name}' created.")
except glue.exceptions.AlreadyExistsException:
    print(f"ℹ Glue database '{database_name}' already exists.")
'''





'''
#Step 3 — Create Glue table from RDS table schema (idher catalog DB me table create kr rhe hain)
#crawler k bagair kia he ya kam manually 

import psycopg2
import boto3

# RDS connection details 
rds_host = "#"
rds_port = "#"
rds_db = "#"
rds_user = "#"
rds_password = "#"

# Glue config 
region_name = "#"
glue_db_name = "#"  
table_name = "#"  # Table to register in Glue

# Connect to RDS 
conn = psycopg2.connect(
    host=rds_host,
    port=rds_port,
    database=rds_db,
    user=rds_user,
    password=rds_password
)
cur = conn.cursor()

# Get column names & types
cur.execute(f"""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = '{table_name}';
""")
columns_info = cur.fetchall()

cur.close()
conn.close()

print(" Columns in RDS table:")
for col, dtype in columns_info:
    print(f"{col} - {dtype}")

#chat gpt ne btaya k ese bhi map kr skte hain without crawler 
# Map Postgres types to Glue types 
type_mapping = {
    "integer": "int",
    "bigint": "bigint",
    "smallint": "smallint",
    "character varying": "string",
    "text": "string",
    "boolean": "boolean",
    "timestamp without time zone": "timestamp",
    "timestamp with time zone": "timestamp",
    "date": "date",
    "double precision": "double",
    "numeric": "decimal"
}

glue_columns = []
for col, dtype in columns_info:
    glue_columns.append({
        "Name": col,
        "Type": type_mapping.get(dtype, "string")  # Default to string
    })

# Create Glue Table 
glue = boto3.client("glue", region_name=region_name)
#chatgpt ne btaya he k ese table create krte hain
try:
    glue.create_table(
        DatabaseName=glue_db_name,
        TableInput={
            "Name": table_name,
            "StorageDescriptor": {
                "Columns": glue_columns,
                "Location": "",  # Not needed for JDBC sources
                "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                "SerdeInfo": {
                    "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe"
                }
            },
            "TableType": "EXTERNAL_TABLE",
            "Parameters": {
                "classification": "postgresql",
                "connectionType": "JDBC"
            }
        }
    )
    print(f" Glue table '{table_name}' created in database '{glue_db_name}'.")
except glue.exceptions.AlreadyExistsException:
    print(f"ℹ Glue table '{table_name}' already exists in database '{glue_db_name}'.")
'''





'''
#  Chunk 1 — Read data from RDS PostgreSQL (based on Glue schema)

import psycopg2
import boto3

# Glue Config 
region_name = "#"
glue_db_name = "#"
glue_table_name = "#"

# RDS PostgreSQL connection 
pg_conn = psycopg2.connect(
    host="#",
    port="#",
    database="#",
    user="#",
    password="#"
)
pg_cur = pg_conn.cursor()

# Get Glue schema
glue = boto3.client("glue", region_name=region_name)
response = glue.get_table(DatabaseName=glue_db_name, Name=glue_table_name)

columns = [col["Name"] for col in response["Table"]["StorageDescriptor"]["Columns"]]
print(" Columns from Glue Catalog:", columns)

# Fetch actual data from PostgreSQL
pg_cur.execute(f"SELECT {', '.join(columns)} FROM {glue_table_name};")
rows = pg_cur.fetchall()

print(f" Retrieved {len(rows)} rows from RDS PostgreSQL.")

pg_cur.close()
pg_conn.close()

'''






'''

#Chunk 2 — Insert into MySQL RDS 
import psycopg2
import pymysql
import boto3

# Glue Config 
region_name = "#"
glue_db_name = "#"
glue_table_name = "#"

# PostgreSQL RDS (source) 
pg_conn = psycopg2.connect(
    host="#",
    port="#",
    database="#",
    user="#",
    password="#"
)
pg_cur = pg_conn.cursor()

# MySQL RDS (target) 
mysql_conn = pymysql.connect(
    host="#",
    port=3306,
    user="#",
    password="#",
    database="#"
)
mysql_cur = mysql_conn.cursor()

# Get Glue schema 
glue = boto3.client("glue", region_name=region_name)
response = glue.get_table(DatabaseName=glue_db_name, Name=glue_table_name)
glue_columns = response["Table"]["StorageDescriptor"]["Columns"]

columns = [col["Name"] for col in glue_columns]
print(" Columns from Glue Catalog:", columns)

# Map Glue types → MySQL types 
type_mapping = {
    "int": "INT",
    "bigint": "BIGINT",
    "smallint": "SMALLINT",
    "string": "VARCHAR(255)",
    "boolean": "BOOLEAN",
    "timestamp": "DATETIME",
    "date": "DATE",
    "double": "DOUBLE",
    "decimal": "DECIMAL(18,2)"
}

# Create table in MySQL if it doesn't exist 
create_table_parts = []
for col in glue_columns:
    mysql_type = type_mapping.get(col["Type"], "VARCHAR(255)")
    create_table_parts.append(f"`{col['Name']}` {mysql_type}")

create_table_sql = f"""
CREATE TABLE IF NOT EXISTS `{glue_table_name}` (
    {', '.join(create_table_parts)}
);
"""
mysql_cur.execute(create_table_sql)
mysql_conn.commit()
print(f"MySQL table '{glue_table_name}' checked/created.")

# Fetch data from PostgreSQL 
pg_cur.execute(f"SELECT {', '.join(columns)} FROM {glue_table_name};")
rows = pg_cur.fetchall()
print(f"Retrieved {len(rows)} rows from RDS PostgreSQL.")

# Insert into MySQL 
placeholders = ", ".join(["%s"] * len(columns))
insert_sql = f"INSERT INTO `{glue_table_name}` ({', '.join(columns)}) VALUES ({placeholders})"

for row in rows:
    mysql_cur.execute(insert_sql, row)

mysql_conn.commit()
print(f"Inserted {len(rows)} rows into MySQL table '{glue_table_name}'.")

# Close connections 
pg_cur.close()
pg_conn.close()
mysql_cur.close()
mysql_conn.close()
'''





'''
#same above step with pyspark 

from pyspark.sql import SparkSession

# Spark session 
spark = SparkSession.builder \
    .appName("PostgresToMySQL") \
    .getOrCreate()

# PostgreSQL RDS (source) 
pg_url = "#"
pg_properties = {
    "user": "#",
    "password": "#",
    "driver": "org.postgresql.Driver"
}

# MySQL RDS (target) 
mysql_url = "#"
mysql_properties = {
    "user": "#",
    "password": "#",
    "driver": "com.mysql.cj.jdbc.Driver"
}

# Table to transfer 
table_name = "#"

# Read from PostgreSQL 
df = spark.read.jdbc(pg_url, table_name, properties=pg_properties)
print("Data read from PostgreSQL RDS")
df.show()

# Write to MySQL 
# Change "append" to "overwrite" if you want to replace the table content
df.write \
    .mode("append") \
    .jdbc(mysql_url, table_name, properties=mysql_properties)

print(f"Data written to MySQL table '{table_name}'")

'''





#to run pyspark job 
'''
spark-submit \
  --jars jars/postgresql-42.2.27.jar,jars/mysql-connector-j-8.0.33.jar \
  RDS-to-RDS.py

''' 