import dlt
import requests
import snowflake.connector


def fetch_api_data():
    """Fetch data from REST API with error handling."""
    url = "https://jsonplaceholder.typicode.com/users"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"📥 Fetched {len(data)} records from API.")
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"❌ Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"❌ Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Unexpected error: {req_err}")
    return []


def get_snowflake_row_count():
    """Query Snowflake to get row count from users table."""
    try:
        conn = snowflake.connector.connect(
            user="sufyan",
            password="xTwfVyLpGK44TDF",
            account="pgdgtoc-ee29791",
            warehouse="etl_warehouse",
            database="etl_db",
            schema="api_data",  # DLT normalized API_DATA to lowercase
            role="ACCOUNTADMIN"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users;")
        row_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return row_count
    except Exception as e:
        print(f"❌ Error querying Snowflake: {e}")
        return None


def run_pipeline():
    """Run DLT pipeline to load API data into Snowflake."""
    # Initialize pipeline
    pipeline = dlt.pipeline(
        pipeline_name="rest_api_to_snowflake",
        destination="snowflake",
        dataset_name="API_DATA"  # Table schema in Snowflake
    )

    # Fetch data
    api_data = fetch_api_data()
    if not api_data:
        print("⚠️ No data fetched. Pipeline aborted.")
        return

    # Run pipeline
    try:
        load_info = pipeline.run(
            api_data,
            table_name="users"  # Target table in Snowflake
        )
        print("✅ Data loaded into Snowflake.")

        # Row count from API source
        api_row_count = len(api_data)
        print(f"📊 API Source Row Count: {api_row_count}")

        # Row count from Snowflake
        snowflake_row_count = get_snowflake_row_count()
        if snowflake_row_count is not None:
            print(f"📊 Snowflake Row Count: {snowflake_row_count}")

            # Compare row counts
            if api_row_count == snowflake_row_count:
                print("✅ OK: Row counts match")
            else:
                print("❌ NOT OK: Row counts do not match")
        else:
            print("⚠️ Could not retrieve row count from Snowflake.")

    except Exception as e:
        print(f"❌ Pipeline error: {e}")


if __name__ == "__main__":
    run_pipeline()
