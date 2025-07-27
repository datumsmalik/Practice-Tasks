from dagster import Definitions
from dagster_demo.assets import fetch_data_asset
from dagster_demo.pipeline import dlt_data_pipeline_job
from dagster_demo.sensors import new_csv_sensor
from dagster_demo.schedules import every_5_minutes_schedule
#from dagster_demo.pipeline import dlt_data_pipeline_job

defs = Definitions(
    assets=[fetch_data_asset],
    jobs=[dlt_data_pipeline_job],
    sensors=[new_csv_sensor],
    schedules=[every_5_minutes_schedule],
)