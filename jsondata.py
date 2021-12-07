import csv
from typing import TextIO

import requests

# HTTP request using GET method
result = requests.get('https://ghibliapi.herokuapp.com/films')

# saving data in JSON format
data = result.json()

# temporary list variable
t_list = []

# Opening the CSV file where I will keep the data
file: TextIO
with open("csv_file.csv", "w", encoding="utf-8-sig") as file:
    header = data[0].keys()

    writer = csv.DictWriter(file, fieldnames=header)
    # defining the header-column in the file

    writer.writeheader()
    # writing the header in the file

    # here data is the list which contains dictionaries data for several movies
    for d in data:
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
                # unpacking the list values and
                # saving in the same column cell
        writer.writerow(d)
