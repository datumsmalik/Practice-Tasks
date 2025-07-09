import json
import pandas as pd
from pandas import json_normalize
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

try:

    logging.info("Loading JSON data from dummy_data.json")
    with open('dummy_data.json') as f:
        data = json.load(f)


    logging.info("Flattening JSON data")
    df = json_normalize(data)

    
    csv_file = 'dummy_data.csv'
    df.to_csv(csv_file, index=False)
    logging.info(f"Flattened JSON data saved as {csv_file}")

except FileNotFoundError as e:
    logging.error(f"File not found: {e.filename}")
except json.JSONDecodeError as e:
    logging.error(f"Invalid JSON format: {e}")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
