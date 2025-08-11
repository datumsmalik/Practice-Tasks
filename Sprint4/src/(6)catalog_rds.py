# Load data from catalog table and put in destination RDS using glue 

from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions

# Initialize Spark + Glue Context
spark = SparkSession.builder.appName("GlueCatalogToPostgres").getOrCreate()
glueContext = GlueContext(spark.sparkContext)
spark = glueContext.spark_session

# Catalog table info
glue_db_name = " pgdatabase-1"
glue_table_name = "sampledata"

# Load data from Glue Catalog table
dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database=glue_db_name,
    table_name=glue_table_name
)

# Convert to Spark DataFrame
df = dynamic_frame.toDF()

# Show a few rows for confirmation
print("Data Preview:")
df.show(5)

# RDS PostgreSQL JDBC connection details
rds_host = "postgres.clwcyeea822i.eu-north-1.rds.amazonaws.com"
rds_port = "5432"
rds_db = "postgres"
rds_user = "postgres"
rds_password = "###"

jdbc_url = f"jdbc:postgresql://{rds_host}:{rds_port}/{rds_db}"

# Write to RDS
df.write \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "glue_exported_table") \
    .option("user", rds_user) \
    .option("password", rds_password) \
    .option("driver", "org.postgresql.Driver") \
    .mode("overwrite") \
    .save()

print(" Successfully written to RDS PostgreSQL.")
