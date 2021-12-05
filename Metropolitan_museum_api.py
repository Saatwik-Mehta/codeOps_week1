import pandas
import requests

data = []


def func(v):
    # v is a list type
    dict_val = []
    for i in v:
        if isinstance(i, dict):  # [12,14,2345,232454] or [key:v, key:{key:v}] or [12,14,2345,232454,key:v]
            for j in i:
                if isinstance(i[j], dict):
                    dict_val.extend(i[j].values())
                else:
                    dict_val.append(i[j])

        else:
            return ','.join(v)
    return ','.join([str(a) for a in dict_val])


objects = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")
d_data = objects.json()
# d_data['objectIDs']
data_cent=d_data['objectIDs'][0:100]

for j in data_cent:

    result = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(j))

    # fetching data in JSON format
    response_data = result.json()

    for i in response_data:
        if isinstance(response_data[i], list):
            response_data[i] = func(response_data[i])

    data.append({i: response_data[i] for i in response_data})

df = pandas.DataFrame(data)

df.to_csv("Metropolitan_Museum_api.csv", encoding="utf-8-sig", index=False, na_rep="None" )
