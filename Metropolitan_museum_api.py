import json
import sys
import pandas
import requests
import csv

data = []



def func(v):
    dict_val = []
    for i in v:
        if isinstance(i, dict):

            print([str(i) for i in i.values()])
            return ','.join([str(i) for i in i.values()])


for j in range(1, 11):
    result = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(j))
    response_data = result.json()
    for i in response_data:
        if isinstance(response_data[i], list):
            if len(response_data[i]):
                response_data[i]=func(response_data[i])
            else:
                response_data[i]=','.join(response_data[i])
    data.append({i: response_data[i] for i in response_data})

df = pandas.DataFrame(data)

df.to_csv("D:/csv_api.csv", encoding="utf-8-sig")
