import pandas as pd
import requests
import json

file_path = "sentimentdataset.csv"


data = pd.read_csv(file_path, sep=";", on_bad_lines="skip", encoding="utf-8")

print(data.head())

url = "https://zhh86kffoi.execute-api.us-east-1.amazonaws.com/test/webhook"


headers = {
    "Content-Type": "application/json",
    "Authorization": "xyz987"
}


for index, row in data.iterrows():
    payload = {"mensaje": row.to_dict()}  
    

    json_payload = json.dumps(payload)


    response = requests.post(url, headers=headers, data=json_payload)
    

    print(f"Fila {index}: {response.status_code}, {response.text}")