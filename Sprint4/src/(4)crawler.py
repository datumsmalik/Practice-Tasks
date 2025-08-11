#Step 3: Create the Glue Crawler

import boto3

glue = boto3.client('glue', region_name='eu-north-1')

crawler_name = 'pg-rds-crawler'
glue_service_role_arn = 'arn:aws:iam::933142127659:role/S3crawlerss'

response = glue.create_crawler(
    Name=crawler_name,
    Role=glue_service_role_arn,
    DatabaseName='pgdatabase2',
    Targets={
        'JdbcTargets': [
            {
                'ConnectionName': 'pg-rds-connection',
                'Path': 'public/%',
                'Exclusions': []
            }
        ]
    },
    TablePrefix='rds_',
    SchemaChangePolicy={
        'UpdateBehavior': 'UPDATE_IN_DATABASE',
        'DeleteBehavior': 'DEPRECATE_IN_DATABASE'
    },
    RecrawlPolicy={
        'RecrawlBehavior': 'CRAWL_EVERYTHING'
    }
)

print(f" Glue crawler '{crawler_name}' created successfully.")
