'''
import dlt
import requests
from datetime import datetime


@dlt.source
def rest_api_source(mode: str = "initial"):
    """
    Fetches API data.
    - 'initial' mode: only first 8 users
    - 'incremental' mode: fetch users 9 and 10
    """
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Add a simulated 'last_updated' timestamp for incremental logic
    for record in data:
        record["last_updated"] = datetime.utcnow().isoformat()

    if mode == "initial":
        # Return only first 8 records
        data_to_load = data[:8]
    elif mode == "incremental":
        # Return records 9 & 10 as new data
        data_to_load = data[8:10]
    else:
        raise ValueError("Invalid mode. Use 'initial' or 'incremental'.")

    print(f"📥 Fetched {len(data_to_load)} records from API (mode={mode})")
    yield dlt.resource(
        data_to_load,
        name="api_users",
        write_disposition="merge",
        primary_key="id"  # 👈 THIS tells DLT how to merge rows
    )
'''


import dlt
import requests
from datetime import datetime


@dlt.source
def rest_api_source(mode: str = "initial"):
    """
    Fetches API data.
    - 'initial' mode: only first 8 users
    - 'incremental' mode: fetch users 9 and 10
    """
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Add a simulated 'last_updated' timestamp
    for record in data:
        record["last_updated"] = datetime.utcnow().isoformat()

    if mode == "initial":
        data_to_load = data[:8]
    elif mode == "incremental":
        data_to_load = data[8:10]  # Simulate only new records
    else:
        raise ValueError("Invalid mode. Use 'initial' or 'incremental'.")

    print(f"📥 Fetched {len(data_to_load)} records from API (mode={mode})")

    yield dlt.resource(
        data_to_load,
        name="api_users",
        primary_key="id",             # Primary key for merge
        write_disposition="merge"     # Enables upserts
    )
