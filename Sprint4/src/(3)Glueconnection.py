import boto3
from botocore.exceptions import ClientError

# Create Glue client
glue = boto3.client('glue', region_name='eu-north-1')

# Optional: delete existing connection
try:
    glue.delete_connection(ConnectionName='pg-rds-connection')
    print(" Existing connection deleted.")
except glue.exceptions.EntityNotFoundException:
    print("ℹ No existing connection to delete.")
except ClientError as e:
    print(f" Unexpected error deleting connection: {e}")

# Create Glue connection with correct driver path and classname
try:
    response = glue.create_connection(
        ConnectionInput={
            'Name': 'pg-rds-connection',
            'ConnectionType': 'JDBC',
            'ConnectionProperties': {
                'JDBC_CONNECTION_URL': 'jdbc:postgresql://postgres.clwcyeea822i.eu-north-1.rds.amazonaws.com:5432/postgres',
                'USERNAME': 'postgres',
                'PASSWORD': '###',

                #  Required for custom driver
                'JDBC_DRIVER_JAR_URI': 's3://localdrivers/postgresql-42.7.3.jar',
                'JDBC_DRIVER_CLASS_NAME': 'org.postgresql.Driver'
            },
            'PhysicalConnectionRequirements': {
                'SubnetId': '###',
                'SecurityGroupIdList': ['###'],
                'AvailabilityZone': 'eu-north-1a'
            }
        }
    )
    print(" Glue connection created successfully.")
except ClientError as e:
    print(f" Failed to create Glue connection: {e}")
