from dagster import ScheduleDefinition
#from dagster_demo.pipeline import process_data_job
from dagster_demo.pipeline import dlt_data_pipeline_job

every_5_minutes_schedule = ScheduleDefinition(
    job=dlt_data_pipeline_job,
    cron_schedule="*/5 * * * *",  # Every 5 minutes
    name="every_5_minutes_schedule",
)
