import json
import csv

# Step 1: Load JSON data
with open('sample.json', 'r') as file:
    json_data = json.load(file)

# Step 2: Flatten manually (no recursion)
flat = {
    "user_id": json_data.get("user", {}).get("id", None),
    "user_name_first": json_data.get("user", {}).get("name", {}).get("first", None),
    "user_name_last": json_data.get("user", {}).get("name", {}).get("last", None),
    "user_location_country": json_data.get("user", {}).get("location", {}).get("country", None),
    "user_location_city_name": json_data.get("user", {}).get("location", {}).get("city", {}).get("name", None),
    "user_location_city_postal_code": json_data.get("user", {}).get("location", {}).get("city", {}).get("postal", {}).get("code", None),
    "user_location_city_postal_area": json_data.get("user", {}).get("location", {}).get("city", {}).get("postal", {}).get("area", None),
    "user_account_created_at": json_data.get("account", {}).get("created_at", None),
    "user_account_status": json_data.get("account", {}).get("status", None)
}


# Step 3: Save to CSV
with open('flattened.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(flat.keys())    # Write header row
    writer.writerow(flat.values())  # Write data row

print("✅ Flattened JSON saved to flattened.csv")
