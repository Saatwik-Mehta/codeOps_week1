import logging
import json
import sys
from apidataprocessing.apidatahandler import ApiDataHandler

if __name__ == '__main__':

    logging.basicConfig(filename='GhibliStudio.log', level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%('
                               'message)s')
    format_dict: dict = {}
    URL = 'https://ghibliapi.herokuapp.com/films'

    try:
        object_to_fetch_data = ApiDataHandler(URL)
        response_data = object_to_fetch_data.request_to_response()
        data = object_to_fetch_data.fetch_nested_link_data(response_data, 'url')
        object_to_fetch_data.json_to_sheets(json_data=data, file_format='csv',
                                            filename='ghibliStudioApi_csv.csv',
                                            encoding='utf-8-sig', index=False, )
        object_to_fetch_data.json_to_sheets(json_data=data, file_format='excel',
                                            filename='ghibliStudioApi_xl.xlsx',
                                            encoding='utf-8-sig', index=False, )
        object_to_fetch_data.json_to_sheets(json_data=data, file_format='xml',
                                            filename='ghibliStudioApi_xml.xml',
                                            encoding='utf-8', index=False, )

        # Converting the image to image-url so that Browsers can render it

        def path_to_image_html(path):
            return '<img src="' + path + '" width="150" height="150" class="img-fluid rounded" >'


        for image_col in ['image', 'movie_banner']:
            format_dict[image_col] = path_to_image_html
        html_string = '''<html> <head><title>HTML Pandas Dataframe with CSS</title>
        </head> <link rel="stylesheet" 
        href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css" 
        integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn" 
        crossorigin="anonymous"> 
        <link rel="stylesheet" type="text/css" href="df_style.css"/> <script 
        src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" 
        integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" 
        crossorigin="anonymous"></script> <script 
        src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" 
        integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" 
        crossorigin="anonymous"></script> <script 
        src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.min.js" 
        integrity="sha384-VHvPCCyXqtD5DqJeNxl2dtTyhF78xXNXdkwX1CZeRusQfRKp+tA7hAShOK/B/fQ2" 
        crossorigin="anonymous"></script> <body> <div class="table-responsive-lg"> 
        {table} </div> </body> </html> '''

        object_to_fetch_data.json_to_html(json_data=data,
                                          filename='ghibliStudioApi_html.html',
                                          encoding='utf-8-sig', index=False, escape=False,
                                          format_dict_arg=format_dict, html_string_arg=html_string,
                                          render_links=True,
                                          classes='table table-striped table-bordered '
                                                  'table-hover table-sm',
                                          columns=['id', 'title', 'original_title',
                                                   'image', 'director', 'producer', 'release_date',
                                                   'running_time', 'people', 'species',
                                                   'locations', 'vehicles'])

        object_to_fetch_data.htmltopdf(html_file='ghibliStudioApi_html.html',
                                       pdf_file='ghibliStudioApi_pdf.pdf',
                                       options={'orientation': 'Landscape', 'page-size': 'A3',
                                                'user-style-sheet': '.\\df_style.css'})

    except TypeError as te:
        logging.error('%s: %s', {te.__class__.__name__}, {te})
        sys.exit(1)
    except json.JSONDecodeError as jde:
        logging.error('%s: %s', {jde.__class__.__name__}, {jde})
        sys.exit(1)
