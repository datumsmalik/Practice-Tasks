import boto3

# Initialize Glue client with your AWS profile & region
session = boto3.Session(
    aws_access_key_id="###",
    aws_secret_access_key="###",
    region_name="eu-north-1"
)
glue_client = session.client('glue')

# Start the Glue job with configurations
response = glue_client.start_job_run(
    JobName="catalog-rds",
    WorkerType="G.1X",            
    NumberOfWorkers=2,
    Timeout=30,                   # in minutes
    ExecutionClass="STANDARD",    # or "FLEX"
    Arguments={
        "--enable-metrics": "true",
        "--enable-continuous-cloudwatch-log": "true",
        "--enable-spark-ui": "true",
        "--spark-event-logs-path": "s3://your-bucket/spark-logs/",
        "--job-language": "python"
    }
)

print(f"Started Glue job run: {response['JobRunId']}")



#Default mode.
#Glue starts your job immediately (as soon as resources are available — usually seconds).

#FLEX
#Glue uses spare capacity in AWS’s infrastructure.
#Jobs might wait in the queue for minutes (sometimes longer) before starting.
