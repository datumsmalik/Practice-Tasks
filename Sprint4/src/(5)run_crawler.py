import boto3
import time
from botocore.exceptions import ClientError

client = boto3.client('glue', region_name='eu-north-1')
crawler_name = 'pg-rds-crawler'

try:
    # Step 1: Start crawler
    response = client.start_crawler(Name=crawler_name)
    print(f" Crawler '{crawler_name}' started successfully.")
except client.exceptions.CrawlerRunningException:
    print(f" Crawler '{crawler_name}' is already running.")
    exit(1)
except client.exceptions.EntityNotFoundException:
    print(f" Crawler '{crawler_name}' not found.")
    exit(1)
except client.exceptions.OperationTimeoutException:
    print(" Operation timed out while starting the crawler.")
    exit(1)
except ClientError as e:
    print(f" Unexpected error: {e}")
    exit(1)

# Step 2: Wait and check status
print(" Waiting for crawler to complete...")

while True:
    crawler = client.get_crawler(Name=crawler_name)['Crawler']
    state = crawler['State']
    role=crawler['Role']

    if state == 'READY':
        print(" Crawler has finished.")
        # Check crawl result
        last_crawl = crawler.get('LastCrawl', {})
        if 'ErrorMessage' in last_crawl:
            print(" Crawler ended with error:")
            print(last_crawl['ErrorMessage'])
        else:
            print("Crawler completed successfully with no errors.")
        break

    elif state == 'RUNNING':
        print(" Crawler is still running...")
    elif state == 'STOPPING':
        print("Crawler is stopping...")
    elif state == 'FAILED':
        print(" Crawler failed to run.")
        last_crawl = crawler.get('LastCrawl', {})
        error_msg = last_crawl.get('ErrorMessage', 'No error message found.')
        print("Error Message:", error_msg)
        break

    print(role)

    time.sleep(5)
