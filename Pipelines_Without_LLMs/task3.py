#now we create a pipeline using DLT hub to load data from restapi to postgres

import dlt  
import requests  # for fetching API data


#sab se pehle source define krte hain
@dlt.source
def src():  
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    data = response.json()  # convert API response to Python list
    return dlt.resource(data, name="testing")  # ab ye data pipline ka hissa ban jayega 


#ab pipline create krte hain
pipline = dlt.pipeline(
        pipeline_name="apne_hath_ki_likhi_pipeline",
        destination="postgres",
        dataset_name="public"  # ye schema he 
 )


#chalo ab pipline run krte hain
load_info = pipline.run(src())
print(f"{load_info.loads_ids}data load ho gaya mubarak ho") #load id kahin par show nahi hp ga sirf piplein ko track krne k lie he


# ab hamain table define krne ki zaroorat hi nai pari DLT khud ye kam krta he 

