#Step 1 Create Glue Database
import boto3

glue = boto3.client('glue', region_name='eu-north-1')  # Change if needed

response = glue.create_database(
    DatabaseInput={
        'Name': 'pgdatabase2'
    }
)

print(" Glue database created:", response)
