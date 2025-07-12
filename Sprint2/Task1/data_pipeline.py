# i have learned how to create a pipeline 


'''import dlt
import pandas as pd

# 1️⃣ Read CSV data
df = pd.read_csv("sample_data.csv")
data = df.to_dict(orient="records")

# 2️⃣ Create the dlt pipeline
pipeline = dlt.pipeline(
    pipeline_name="csv_pipeline",
    destination="postgres",  # Destination: PostgreSQL
    dataset_name="csv_data"  # Schema name in Postgres
)

# 3️⃣ Run the pipeline
load_info = pipeline.run(data, table_name="my_table")

print("✅ Data loaded successfully!")
print(load_info)
'''
#in this task we have created a pipeline to load data from a csv file to a postgres database and we have also used the backfill feature to load the data again

import dlt
import pandas as pd

# Load CSV data
df = pd.read_csv("sample_data.csv")
data = df.to_dict(orient="records")

# Create pipeline
pipeline = dlt.pipeline(
    pipeline_name="csv_pipeline",
    destination="postgres",
    dataset_name="csv_data"
)

# Force a backfill by dropping the state
pipeline.drop()

# Run the pipeline
load_info = pipeline.run(data, table_name="my_table")

print("✅ Backfill completed. All data reloaded.")
print(load_info)
