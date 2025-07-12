#in this task we have created a pipeline to load data from clickup to a postgres database 


'''import requests

# Your API token and list_id
api_token = "pk_94778220_PC6NBBICTMTP07S74M3F1UP3Z9LWL65T"
list_id = "901513164674"

# URL for Get Tasks endpoint
url = f"https://api.clickup.com/api/v2/list/{list_id}/task"

# Headers
headers = {
    "Authorization": api_token,
    "accept": "application/json"
}

# Make GET request
response = requests.get(url, headers=headers)

# Check response
if response.status_code == 200:
    tasks = response.json()["tasks"]
    print(f"✅ Found {len(tasks)} tasks in list {list_id}:")
    for task in tasks:
        print(f"- {task['name']} (ID: {task['id']})")
else:
    print("❌ Error:", response.status_code, response.text)
'''


import dlt
import requests

@dlt.source
def clickup_source():
    # Your API token and list_id
    api_token = "pk_94778220_PC6NBBICTMTP07S74M3F1UP3Z9LWL65T"
    list_id = "901513164673"  # Your actual list_id

    headers = {
        "Authorization": api_token,
        "accept": "application/json"
    }

    @dlt.resource
    def tasks():
        url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
        response = requests.get(url, headers=headers)

        # Check for errors
        if response.status_code != 200:
            print(f"❌ Failed to fetch data: {response.status_code} {response.text}")
            return

        # Parse tasks
        tasks_data = response.json().get("tasks", [])
        print(f"\n✅ Found {len(tasks_data)} tasks in ClickUp list {list_id}:")
        for task in tasks_data:
            print(f"- {task.get('name')} (ID: {task.get('id')})")

        # Yield tasks to DLT
        yield tasks_data

    return tasks


# Create the pipeline
pipeline = dlt.pipeline(
    pipeline_name="clickup_pipeline",
    destination="postgres",  # Use postgres as destination
    dataset_name="clickup_data"  # The schema name in Postgres
)

# Run the pipeline
load_info = pipeline.run(
    clickup_source(),
    table_name="clickup_tasks"  # Table name in Postgres
)

# Print pipeline summary
print("\n✅ Pipeline executed successfully!")
print(load_info)
