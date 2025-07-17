import dlt
import requests
import snowflake.connector


def fetch_nested_api_data():
    """Fetch nested JSON data from REST API with error handling."""
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


def flatten_data(nested_data):
    """Flatten nested fields in JSON into a flat structure."""
    flat_records = []
    for user in nested_data:
        flat_record = {
            "id": user.get("id"),
            "name": user.get("name"),
            "username": user.get("username"),
            "email": user.get("email"),
            # Flatten nested address
            "address_street": user.get("address", {}).get("street"),
            "address_suite": user.get("address", {}).get("suite"),
            "address_city": user.get("address", {}).get("city"),
            "address_zipcode": user.get("address", {}).get("zipcode"),
            "address_geo_lat": user.get("address", {}).get("geo", {}).get("lat"),
            "address_geo_lng": user.get("address", {}).get("geo", {}).get("lng"),
            # Flatten nested company
            "company_name": user.get("company", {}).get("name"),
            "company_catch_phrase": user.get("company", {}).get("catchPhrase"),
            "company_bs": user.get("company", {}).get("bs"),
            "phone": user.get("phone"),
            "website": user.get("website"),
        }
        flat_records.append(flat_record)
    return flat_records


def get_snowflake_row_count():
    """Query Snowflake to get row count from nested table."""
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
        cursor.execute("SELECT COUNT(*) FROM nested;")
        row_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return row_count
    except Exception as e:
        print(f"❌ Error querying Snowflake: {e}")
        return None


def run_pipeline():
    """Run DLT pipeline to load flattened nested data into Snowflake."""
    # Initialize pipeline
    pipeline = dlt.pipeline(
        pipeline_name="nested_api_to_snowflake",
        destination="snowflake",
        dataset_name="API_DATA"  # Table schema in Snowflake
    )

    # Fetch and flatten data
    nested_data = fetch_nested_api_data()
    if not nested_data:
        print("⚠️ No data fetched. Pipeline aborted.")
        return
    flat_data = flatten_data(nested_data)

    # Run pipeline
    try:
        load_info = pipeline.run(
            flat_data,
            table_name="nested"  # Target table in Snowflake
        )
        print("✅ Flattened data loaded into Snowflake.")

        # Row count from API source
        api_row_count = len(flat_data)
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
