import requests
import pandas
from IPython.core.display import display, HTML
import pdfkit

t_list = []

# HTTP request using GET method
result = requests.get('https://ghibliapi.herokuapp.com/films')

response_data = result.json()

for d in response_data:
    for i in d:

        if isinstance(d[i], list):
            # d[i] is the dict->values-list that
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
                        # Fetching the value from key->name of the dictionary

                    elif isinstance(data_fmt, list):
                        for a in data_fmt:
                            if d['url'] in a['films']:
                                t_list.append(a['name'])
                        d[i] = t_list
                        t_list = []
                except requests.ConnectionError as e:
                    # If hyperlink is not in the list except-block will be executed with nothing
                    pass

            d[i] = ','.join(d[i])
            # Unpacking list items and saving as strings

data = []
# Saving data in JSON format

for data_dict in response_data:
    data.append({i: data_dict[i] for i in data_dict})

# Saving data as DataFrame
df = pandas.DataFrame(data)


def path_to_image_html(path):
    return '<img src="' + path + '" width="150" height="150" class="img-fluid rounded" >'


# Converting the image url so that Browsers can render it
image_cols = ['image', 'movie_banner']
format_dict = {}
pandas.set_option('display.max_colwidth', None)

for image_col in image_cols:
    format_dict[image_col] = path_to_image_html

# Final process of converting the files into respective format(HTML, CSV, PDF, Excel, XML)

html_string = '''<html> <head><title>HTML Pandas Dataframe with CSS</title></head> <link rel="stylesheet" 
href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css" 
integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn" crossorigin="anonymous"> <link 
rel="stylesheet" type="text/css" href="df_style.css"/> <script 
src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" 
integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script> 
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" 
integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script> 
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.min.js" 
integrity="sha384-VHvPCCyXqtD5DqJeNxl2dtTyhF78xXNXdkwX1CZeRusQfRKp+tA7hAShOK/B/fQ2" crossorigin="anonymous"></script> 
<body> <div class="table-responsive-lg"> {table} </div> </body> </html> '''

display(HTML(df.to_html(escape=False, formatters=format_dict)))

with open("ghibliStudioApi_html.html", "w", encoding="utf-8-sig") as f:
    f.write(html_string.format(table=df.to_html(index=False, escape=False, formatters=format_dict, render_links=True,
                                                classes="table table-striped table-bordered table-hover table-sm",
                                                columns=['id', 'title', 'original_title', 'image', 'director',
                                                         'producer', 'release_date', 'running_time', 'people',
                                                         'species', 'locations', 'vehicles'])))

df.to_csv("ghibliStudioApi_csv.csv", encoding="utf-8-sig", index=False)
config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
pdfkit.from_file('ghibliStudioApi_html.html', 'ghibliStudioApi_pdf.pdf', configuration=config,
                 options={"orientation": "Landscape", "page-size": "A3", 'user-style-sheet': 'C:\\Users\\Saatwik '
                                                                                             'Mehta\\PycharmProjects'
                                                                                             '\\codeOps_week1'
                                                                                             '\\df_style.css'})
df.to_excel("ghibliStudioApi_xl.xlsx", encoding="utf-8-sig", index=False)
df.to_xml("ghibliStudioApi_xml.xml", index=False)
