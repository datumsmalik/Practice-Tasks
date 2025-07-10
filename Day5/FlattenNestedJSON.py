import json
import pandas as pd
from pandas import json_normalize

# Load JSON (simulate reading from file)
with open('sample_data.json') as f:
    data = json.load(f)

# Flatten JSON
df = json_normalize(
    data,
    record_path='orders',           # Flatten the nested "orders" list
    meta=['id', 'name', ['contact', 'email'], ['contact', 'phone']] # Keep these as metadata
)

# Save to CSV
df.to_csv('flattened_data.csv', index=False)

print("✅ Nested JSON flattened and saved as flattened_data.csv")
print(df)
