
#Step 1 — Create Glue table from RDS table schema (idher catalog DB me table create kr rhe hain)
#crawler k bagair kia he ya kam manually 

import psycopg2
import boto3

# RDS connection details 
rds_host = "postgres.clwcyeea822i.eu-north-1.rds.amazonaws.com"
rds_port = "5432"
rds_db = "postgres"
rds_user = "postgres"
rds_password = "Paki$tani123$$$"

# Glue config 
region_name = "eu-north-1"
glue_db_name = "rdbsql"  
table_name = "books"  # Table to register in Glue

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


