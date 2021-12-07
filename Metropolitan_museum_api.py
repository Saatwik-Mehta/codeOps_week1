import pandas
import requests

data = []


def func(v):
    dict_val = []
    for item in v:
        if isinstance(item, dict):
            for item_value in item:
                if isinstance(item[item_value], dict):
                    dict_val.extend(item[item_value].values())
                else:
                    dict_val.append(item[item_value])

        else:
            return ','.join(v)
    return ','.join([str(a) for a in dict_val])


# Fetching first 100 object-IDs
objects = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")
d_data = objects.json()
data_cent = d_data['objectIDs'][0:100]

# Fetching the data of first 100 objects with their ID
for j in data_cent:

    result = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(j))
    response_data = result.json()

    for i in response_data:
        if isinstance(response_data[i], list):
            # Using function -> func to retrieve data values from dictionary
            response_data[i] = func(response_data[i])

    # Saving the modified data
    data.append({i: response_data[i] for i in response_data})

df = pandas.DataFrame(data)
df.to_csv("Metropolitan_Museum_api.csv", encoding="utf-8-sig", index=False, na_rep="None")
