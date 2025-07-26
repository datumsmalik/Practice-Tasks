from dagster import sensor, RunRequest
import os

WATCH_FOLDER = "./watch_folder"  # folder to watch for new CSVs

@sensor(job_name="dlt_data_pipeline_job")
def new_csv_sensor(context):
    """Detect new CSV files in WATCH_FOLDER and trigger job."""
    if not os.path.exists(WATCH_FOLDER):
        os.makedirs(WATCH_FOLDER)

    csv_files = [f for f in os.listdir(WATCH_FOLDER) if f.endswith(".csv")]  # filters only file that ends with csv
    if not csv_files:
        context.log.info("No new CSV files found.")
        return

    for csv_file in csv_files:
        context.log.info(f"New CSV file detected: {csv_file}")
        yield RunRequest(run_key=csv_file)
