from dagster import asset
import pandas as pd

@asset
def fetch_data_asset():
    """Fetch random data and save it to data.csv"""
    data = {
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35]
    }
    df = pd.DataFrame(data)
    df.to_csv("data.csv", index=False)
    print("Asset: data.csv created")
    return "data.csv"




#ASSET DATA MATERIALZE KR K CSV FILE SAVE KRTA HE
#phir op us data me ELT/DLT pipeline k zarye 1 clomn add krte hain or data ko destination pe bhegte hain
#sensor sense krta he k agar watch folder me koi nai file add kro ge to me bta dun ga or destination chala jae ga data
#schdeuler pipline ko har 5 din bad run kre gi