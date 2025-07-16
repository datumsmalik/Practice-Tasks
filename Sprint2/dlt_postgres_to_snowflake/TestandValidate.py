#in this task we are going to test and validate the data from postgres and validate row counts
import psycopg2
import pandas as pd

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="sufyan",
    user="postgres",
    password="pakistan",
    host="localhost",
    port=5432
)
conn.autocommit = True
cur = conn.cursor()

# Extract data from source_table
df = pd.read_sql("SELECT * FROM source_table", conn)
print(f"Extracted {len(df)} rows from source_table")

# Load data into destination_table
for _, row in df.iterrows():
    cur.execute(
        "INSERT INTO destination_table (name) VALUES (%s)", 
        (row['name'],)
    )

# Validate row counts
cur.execute("SELECT COUNT(*) FROM source_table")
source_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM destination_table")
dest_count = cur.fetchone()[0]

if source_count == dest_count:
    print(f"✅ Row count matches: {source_count} rows")
else:
    print(f"❌ Row count mismatch: source={source_count}, destination={dest_count}")

# Cleanup
cur.close()
conn.close()
