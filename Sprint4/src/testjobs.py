import pytest # Finds test functions automatically 
from pyspark.sql import SparkSession
from awsglue.context import GlueContext

# AWS Glue Catalog table info
GLUE_DB_NAME = " pgdatabase-1"  
GLUE_TABLE_NAME = "sampledata"

@pytest.fixture(scope="module")  #"Run this function before my test starts, give me whatever it returns, and clean it up afterward."

# scope=module means runs once per Python test file (.py module).


#Without enableHiveSupport(), Spark doesn’t know how to query tables from the Glue Catalog using the from_catalog() method (or SQL queries on Glue tables).
#With scope="module", Spark starts once and is reused by all tests in that file.



def spark():
    spark = SparkSession.builder \
        .appName("GlueJobPyTest") \
        .enableHiveSupport() \
        .getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture(scope="module")
def glue_df(spark):
    # Create GlueContext
    glue_context = GlueContext(spark.sparkContext)

    # Load data from Glue Catalog
    dynamic_frame = glue_context.create_dynamic_frame.from_catalog(
        database=GLUE_DB_NAME,
        table_name=GLUE_TABLE_NAME
    )

    # Convert to Spark DataFrame
    return dynamic_frame.toDF()

def test_males_present(glue_df):
    male_names = {"Ali", "Ahmed", "Hassan", "Omar"}

    names_in_data = {row["name"] for row in glue_df.collect()}
    males_found = names_in_data.intersection(male_names)

    print(f"Males found in Glue table: {males_found}")
    assert len(males_found) > 0, "No male names found in Glue Catalog dataset"

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v", "-s"]))

#"-v" = verbose mode (shows each test name + result).

#"-s" = lets print() statements inside tests actually show in output.

