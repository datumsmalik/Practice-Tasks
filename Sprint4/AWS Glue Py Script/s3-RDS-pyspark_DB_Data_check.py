import psycopg2

# RDS connection details
rds_host = "postgres.clwcyeea822i.eu-north-1.rds.amazonaws.com"
rds_port = "5432"
rds_db = "postgres"
rds_user = "postgres"  # Replace with your RDS master username
rds_password = "Paki$tani123$$$"

# Connect to RDS PostgreSQL
conn = psycopg2.connect(
    host=rds_host,
    port=rds_port,
    database=rds_db,
    user=rds_user,
    password=rds_password
)

cur = conn.cursor()

# Fetch rows from target table
cur.execute("SELECT * FROM sampledata_target;")
rows = cur.fetchall()

print(" Data in sampledata_target table:")
for row in rows:
    print(row)

# Optionally check row count
cur.execute("SELECT COUNT(*) FROM sampledata_target;")
count = cur.fetchone()[0]
print(f"\n Total rows in table: {count}")

cur.close()
conn.close()
