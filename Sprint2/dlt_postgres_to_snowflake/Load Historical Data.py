#in this task we are going to extract data from postgres and load it into snowflake

'''import psycopg2
import snowflake.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Postgres connection parameters
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_USERNAME = os.getenv("PG_USERNAME")
PG_PASSWORD = os.getenv("PG_PASSWORD")

# Snowflake connection parameters
SF_USER = os.getenv("SNOWFLAKE_USER")
SF_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SF_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SF_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SF_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SF_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SF_ROLE = os.getenv("SNOWFLAKE_ROLE")

# Step 1: Extract data from Postgres
def extract_from_postgres():
    print("Connecting to Postgres...")
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DATABASE,
        user=PG_USERNAME,
        password=PG_PASSWORD
    )
    cur = conn.cursor()
    # Set schema for Postgres
    cur.execute("SET search_path TO clickup_data;")
    cur.execute("SELECT * FROM clickup_tasks;")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    print(f"✅ Extracted {len(rows)} rows from Postgres")
    return rows, columns

# Step 2: Load data into Snowflake
def load_into_snowflake(rows, columns):
    print("Connecting to Snowflake...")
    ctx = snowflake.connector.connect(
        user=SF_USER,
        password=SF_PASSWORD,
        account=SF_ACCOUNT,
        warehouse=SF_WAREHOUSE,
        database=SF_DATABASE,
        schema=SF_SCHEMA,
        role=SF_ROLE
    )
    cs = ctx.cursor()

    # Set database and schema for the session
    cs.execute(f"USE DATABASE {SF_DATABASE}")
    cs.execute(f"USE SCHEMA {SF_SCHEMA}")

    # Create table in Snowflake if not exists
    columns_sql = ", ".join([f"{col} STRING" for col in columns])
    create_table_sql = f"""
    CREATE OR REPLACE TABLE clickup_tasks ({columns_sql});
    """
    cs.execute(create_table_sql)
    print("✅ Snowflake table created/replaced.")

    # Insert data into Snowflake
    insert_sql = f"""
    INSERT INTO clickup_tasks ({", ".join(columns)})
    VALUES ({", ".join(['%s' for _ in columns])});
    """
    cs.executemany(insert_sql, rows)
    ctx.commit()
    cs.close()
    ctx.close()
    print(f"✅ Loaded {len(rows)} rows into Snowflake.")

if __name__ == "__main__":
    data, columns = extract_from_postgres()
    load_into_snowflake(data, columns)
'''
import dlt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Postgres connection parameters
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_USERNAME = os.getenv("PG_USERNAME")
PG_PASSWORD = os.getenv("PG_PASSWORD")

# Step 1: Extract data from Postgres
@dlt.source
def postgres_source():
    @dlt.resource(write_disposition="replace")  # Replace table for demo
    def clickup_tasks():
        import psycopg2

        print("Connecting to Postgres...")
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            dbname=PG_DATABASE,
            user=PG_USERNAME,
            password=PG_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("SET search_path TO clickup_data;")
        cur.execute("SELECT * FROM clickup_tasks;")
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        cur.close()
        conn.close()
        print(f"✅ Extracted {len(rows)} rows from Postgres")

        # Yield rows as dicts for DLT
        for row in rows:
            yield dict(zip(columns, row))

    return clickup_tasks

# Step 2: Load data into Snowflake
if __name__ == "__main__":
    print("🚀 Starting DLT pipeline...")

    # 🚨 Removed credentials=, DLT will auto-load from .dlt/secrets.toml
    pipeline = dlt.pipeline(
        pipeline_name="pg_to_snowflake",
        destination="snowflake",
        dataset_name="clickup_tasks"  # Snowflake schema name
    )

    load_info = pipeline.run(
        postgres_source(),
        write_disposition="replace"
    )

    print(f"✅ Loaded data into Snowflake: {load_info}")
