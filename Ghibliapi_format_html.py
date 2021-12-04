
import requests
import pandas

# HTTP request using GET method
t_list=[]
result = requests.get('https://ghibliapi.herokuapp.com/films')
response_data = result.json()
for d in response_data:
    for i in d:

        if isinstance(d[i], list):
            # d[i] is the dict->values list that
            # contains values of several key fields
            # such as people, location, species and vehicles.

            for j in d[i]:
                # Iterating through each list item
                # and verifying if it is a hyperlink.

                try:
                    rs = requests.get(j)
                    data_fmt = rs.json()

                    if isinstance(data_fmt, dict):
                        d[i][d[i].index(j)] = data_fmt['name']

                    elif isinstance(data_fmt, list):
                        for a in data_fmt:
                            if d['url'] in a['films']:
                                # url link of movie in cells list's element(hyperlink!)

                                t_list.append(a['name'])
                        d[i] = t_list
                        t_list = []
                except requests.ConnectionError as e:
                    pass

            d[i] = ','.join(d[i])

data = []
# saving data in JSON format
for data_dict in response_data:
    data.append({i: data_dict[i] for i in data_dict})

df = pandas.DataFrame(data)
df.to_csv("ghibliStudioApi.csv", encoding="utf-8-sig")
df.to_html("ghibliStudioApi.html", encoding="utf-8-sig")
df.to_excel("ghibliStudioApi.xlsx", encoding="utf-8-sig")
df.to_xml("ghibliStudioApi.xlsx", encoding="utf-8-sig")
# temporary list variable

