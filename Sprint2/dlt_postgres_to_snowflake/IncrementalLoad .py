#in this task we are going to load incremental data from postgres to postgress just to test the incremental load
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

# ✅ Ensure destination_table exists
cur.execute("""
CREATE TABLE IF NOT EXISTS destination_table (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

# 📥 Extract data from source_table
df = pd.read_sql("SELECT * FROM source_table", conn)
print(f"📥 Extracted {len(df)} rows from source_table")

# 🔁 Insert only rows that don’t exist in destination_table
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO destination_table (id, name)
        VALUES (%s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (row['id'], row['name']))

print(f"✅ Incremental load completed: {len(df)} rows processed")

# ✅ Validate row counts
cur.execute("SELECT COUNT(*) FROM source_table")
source_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM destination_table")
dest_count = cur.fetchone()[0]

print(f"🔍 Source rows: {source_count} | Destination rows: {dest_count}")

# 🔒 Cleanup
cur.close()
conn.close()
