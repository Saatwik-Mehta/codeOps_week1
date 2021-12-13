import logging
import json
import sys
import pandas
import fetchapidata
import getflatlist
import jsonconverter
import pdfgenerator

if __name__ == '__main__':

    logging.basicConfig(filename="GhibliStudio.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%("
                                                                                "message)s")
    data = []
    format_dict = {}
    URL = 'https://ghibliapi.herokuapp.com/films'

    try:
        response_data = fetchapidata.request_to_response(URL)

        for film_dict_data in response_data:
            for column in film_dict_data:
                if isinstance(film_dict_data[column], list):
                    extracted_data = getflatlist.extract_data(film_dict_data[column], film_dict_data['url'])

                    if extracted_data is not None:
                        film_dict_data[column] = ','.join(extracted_data)
                    else:
                        film_dict_data[column] = ''
                if film_dict_data[column] is None:
                    film_dict_data[column] = ''

        for data_dict in response_data:
            data.append({i: data_dict[i] for i in data_dict})

    except TypeError as te:
        logging.error(f"{te.__class__.__name__}: {te}")
        sys.exit(1)

    except json.JSONDecodeError as jde:
        logging.error(f"{jde.__class__.__name__}: {jde}")
        sys.exit(1)

    df = pandas.DataFrame(data)

    # Converting the image to image-url so that Browsers can render it
    image_cols = ['image', 'movie_banner']
    pandas.set_option('display.max_colwidth', None)


    def path_to_image_html(path):
        return '<img src="' + path + '" width="150" height="150" class="img-fluid rounded" >'


    for image_col in image_cols:
        format_dict[image_col] = path_to_image_html

    html_string = '''<html> <head><title>HTML Pandas Dataframe with CSS</title></head> <link rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"
    integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="df_style.css"/> <script
    src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"
    integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
    crossorigin="anonymous"></script> <script
    src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"
    integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN"
    crossorigin="anonymous"></script> <script
    src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.min.js"
    integrity="sha384-VHvPCCyXqtD5DqJeNxl2dtTyhF78xXNXdkwX1CZeRusQfRKp+tA7hAShOK/B/fQ2"
    crossorigin="anonymous"></script> <body> <div class="table-responsive-lg"> {table} </div> </body> </html> '''

    # Final process of converting the files into respective format(HTML, CSV, PDF, Excel, XML)
    jsonconverter.jsontocsv(dataframe=df, filename="ghibliStudioApi_csv.csv", encoding="utf-8-sig", index=False)
    jsonconverter.jsontoexcel(dataframe=df, filename="ghibliStudioApi_xl.xlsx", encoding="utf-8-sig", index=False)
    jsonconverter.jsontoxml(dataframe=df, filename="ghibliStudioApi_xml.xml", index=False)
    jsonconverter.jsontohtml(dataframe=df, filename="ghibliStudioApi_html.html", escape=False, encoding="utf-8-sig",
                             format_dict_arg=format_dict, html_string_arg=html_string, index=False,
                             render_links=True, classes="table table-striped table-bordered table-hover table-sm",
                             columns=['id', 'title', 'original_title', 'image', 'director', 'producer', 'release_date',
                                      'running_time', 'people', 'species', 'locations', 'vehicles'])

    css_path = '.\\df_style.css'
    pdfgenerator.htmltopdf('ghibliStudioApi_html.html', 'ghibliStudioApi_pdf.pdf',
                           options={"orientation": "Landscape",
                                    "page-size": "A3",
                                    'user-style-sheet': css_path})
