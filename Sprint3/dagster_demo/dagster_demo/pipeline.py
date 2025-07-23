# ye pipeline ELT k sath he 

'''
from dagster import op, job
import pandas as pd

@op
def process_data_op():
    """Read data.csv, add a new column, and save processed_data.csv"""
    # Read data
    df = pd.read_csv("data.csv")

    # Add new column
    df["salary"] = [50000, 60000, 70000]

    # Save to new CSV
    df.to_csv("processed_data.csv", index=False)
    print("✅ Op: processed_data.csv created")

    return "processed_data.csv"

@job
def process_data_job():
    process_data_op()
'''

# ye pipeline DLT k sath he 

import dlt
import pandas as pd
from dagster import op, job


@op
def dlt_pipeline_op():
    """
    DLT pipeline: Reads data.csv, processes it, saves processed_data.csv,
    and loads it into Snowflake.
    """
    # Step 1: Read existing CSV
    df = pd.read_csv("data.csv")
    print("✅ Read data.csv:")
    print(df)

    # Step 2: Add a new column
    df["salary"] = [50000, 60000, 70000]
    print("✅ Added salary column.")

    # Step 3: Save processed data
    processed_file = "processed_data.csv"
    df.to_csv(processed_file, index=False)
    print(f"✅ Processed data saved to {processed_file}")

    # Step 4: Send data to Snowflake
    # DLT automatically loads credentials from secrets.toml
    pipeline = dlt.pipeline(
        pipeline_name="dagster_dlt_pipeline",
        destination="snowflake",
        dataset_name="public",   
    )

    # Load Pandas DataFrame into DLT
    load_info = pipeline.run(df, table_name="processed_datahe")
    print(f"✅ Data loaded to Snowflake: {load_info}")

    return processed_file


@job
def dlt_data_pipeline_job():
    dlt_pipeline_op()
