'''
import dlt
from apisource import rest_api_source

# Initialize pipeline
pipeline = dlt.pipeline(
    pipeline_name="rest_api_to_snowflake",
    destination="snowflake",
    dataset_name="API_DATA"  # Table schema in Snowflake
)

# Change mode: "initial" for first run, "incremental" for new data
mode = "initial"

# Run pipeline
info = pipeline.run(
    rest_api_source(mode),
    table_name="API_DATA",
    write_disposition="merge"  # Enables incremental updates
)

print("✅ Data loaded into Snowflake:")
print(info)
'''

import dlt
from apisource import rest_api_source

# Initialize pipeline
pipeline = dlt.pipeline(
    pipeline_name="rest_api_to_snowflake",
    destination="snowflake",
    dataset_name="API_DATA"  # Table schema in Snowflake
)

# Change mode here
mode = "incremental"

# Run pipeline
info = pipeline.run(
    rest_api_source(mode),
    table_name="API_DATA",
    write_disposition="merge"  # Enables incremental updates
)

print("✅ Data loaded into Snowflake:")
print(info)
