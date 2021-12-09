import logging
import json
import os.path
import sys
from typing import Sequence
import requests
import pandas
from IPython.core.display import display, HTML
import pdfkit


def request_to_response(api_url: str):
    """
    This function is used to convert the requested API data
    into JSON format for data processing
    :param api_url: This parameter take the website URL in string format
                    eg: "http://somesiteapi.com/somedatatofetch?"
    :return: Returning data will be in Json format for data processing.
    """

    if isinstance(api_url, str):
        try:
            result = requests.get(api_url)
        except requests.exceptions.MissingSchema as ms:
            logging.error(f"{ms.__class__.__name__}: {ms}")
        except requests.ConnectionError as rce:
            logging.error(f"{rce.__class__.__name__}: {rce}")
            logging.info("Couldn't make the connection")
            sys.exit(1)
        else:
            result_data = result.json()
            return result_data


def extract_data(data_list: list, film_url: str = ''):
    """
    This function accepts the list data which may have hyperlinks
    and returns the flattened data that can be added in the data field

    eg: In the field data_list[0]="http://somesiteapi.com/somedatatofetch"
        after accessing, fetches the appropriate data and replaces it with
        hyperlink in data_list[0].

    :param data_list: Accepts list value that needs to be unpacked
    :param film_url: Contains the url of the particular film whose data is being flattened
    :return: return the list with data values only
    """

    global t_list
    if isinstance(data_list, list) and isinstance(film_url, str):
        try:
            for item in data_list:
                rs = requests.get(item)
                item_data = rs.json()

                if isinstance(item_data, dict):
                    data_list[data_list.index(item)] = item_data['name']

                elif isinstance(item_data, list):
                    for item_data_dict in item_data:
                        if film_url in item_data_dict['films']:
                            t_list.append(item_data_dict['name'])
                    data_list = t_list
                    t_list = []
        except requests.ConnectionError as ae:
            logging.error(f"{ae.__class__.__name__}: {ae}")
            logging.info(f"Connection Interruption while execution")
            return data_list
        except requests.exceptions.MissingSchema as ms:
            logging.error(f"{ms.__class__.__name__}: {ms}")
            logging.info(f"Not a valid web URL")
            return data_list
    return data_list


def jsontocsv(dataframe, filename, encoding="utf-8", index=False):
    """
    Converts the JSON data fetched from API into CSV format and saves inside the file (filename).
    :param dataframe: Accepts the DataFrame converted from JSON data using pandas library .
    :param filename: User defined filename to save the converted data. It can contain path with filename as well.
    :param encoding: The encoding value user wants to encode the file data.
    :param index: If each row should have and index, default is False.
    :return: None
    """
    if isinstance(dataframe, pandas.DataFrame) and len(dataframe):
        try:
            dataframe.to_csv(filename, encoding=encoding, index=index)
        except PermissionError as pe:
            logging.error(f"{pe.__class__.__name__}: {pe}")
            logging.info(f"Cannot edit the file {filename}")


def jsontoexcel(dataframe, filename, encoding="utf-8", index=False):
    """
    Converts the JSON data fetched from API into Excel format and saves inside the file (filename).
    :param dataframe: Accepts the DataFrame converted from JSON data using pandas library.
    :param filename: User defined filename to save the converted data. It can contain path with filename as well.
    :param encoding: The encoding value user wants to encode the file data.
    :param index: If each row should have and index, default is False
    :return: None
    """
    if isinstance(dataframe, pandas.DataFrame) and len(dataframe):
        try:
            dataframe.to_excel(filename, encoding=encoding, index=index)
        except PermissionError as pe:
            logging.error(f"{pe.__class__.__name__}: {pe}")
            logging.info(f"Cannot edit the file {filename}")


def jsontoxml(dataframe, filename, encoding="utf-8", index=False):
    """
    Converts the JSON data fetched from API into Xml format and saves inside the file (filename).
    :param dataframe: Accepts the DataFrame converted from JSON data using pandas library.
    :param filename: User defined filename to save the converted data. It can contain path with filename as well.
    :param encoding: The encoding value user wants to encode the file data.
    :param index: If each row should have and index, default is False
    :return: None
    """
    if isinstance(dataframe, pandas.DataFrame) and len(dataframe):
        try:
            dataframe.to_xml(filename, encoding=encoding, index=index)
        except PermissionError as pe:
            logging.error(f"{pe.__class__.__name__}: {pe}")
            logging.info(f"Cannot edit the file {filename}")


def jsontohtml(dataframe, filename, escape=False, encoding="utf-8", format_dict_arg=None, html_string_arg="",
               index=False, render_links=True, classes: str = None, columns: Sequence[str] = None):
    """
    Converts the JSON data fetched from API into HTML format and saves inside the file (filename).
    :param dataframe: Accepts the DataFrame converted from JSON data using pandas library.
    :param filename: User defined filename to save the converted data. It can contain path with filename as well.
    :param escape: Convert the characters <, >, and & to HTML-safe sequences
    :param encoding: The encoding value user wants to encode the file data.
    :param format_dict_arg: formatters for HTML elements
    :param html_string_arg: HTML template for the data representation
    :param index: If each row should have and index, default is False
    :param render_links: renders the document URL links to HTML hyperlink
    :param classes: Add classes to HTML template
    :param columns: Data Columns for representation in HTML format
    :return: None
    """

    if isinstance(dataframe, pandas.DataFrame) and len(dataframe):
        try:
            display(HTML(dataframe.to_html(escape=False, formatters=format_dict_arg)))
            with open(filename, mode="w", encoding=encoding) as f:
                f.write(html_string_arg.format(table=dataframe.to_html(index=index, escape=escape,
                                                                       formatters=format_dict,
                                                                       render_links=render_links,
                                                                       classes=classes,
                                                                       columns=columns)))
        except PermissionError as pe:
            logging.error(f"{pe.__class__.__name__}: {pe}")
            logging.info(f"Cannot edit the file {filename}")


def htmltopdf(html_file, pdf_file, pathto_wkhtmltopdf=None, options=None, css=None):
    """
    Using pdfkit library to convert the HTML file into PDF file.
    :param html_file: Path to the HTML file from which PDF file will be generated
    :param pdf_file: User defined filename to save the converted data. It can contain path with filename as well.
    :param pathto_wkhtmltopdf: path to wkhtmltopdf folder[if required]
    :param options: a dict object to format the pdf file
    :param css: css file name to be used in pdf file. Path can also be included (if required).
    :return: None
    """
    if os.path.splitext(html_file)[-1].lower() == '.html' and os.path.isfile(html_file) :
        try:
            config = pdfkit.configuration(wkhtmltopdf=pathto_wkhtmltopdf)
            pdfkit.from_file(html_file, pdf_file, configuration=config, options=options, css=css)

        except PermissionError as pe:
            logging.error(f"{pe.__class__.__name__}: {pe}")
            logging.info(f"Cannot edit the file {pdf_file}")


if __name__ == '__main__':

    logging.basicConfig(filename="GhibliStudio.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%("
                                                                                "message)s")
    # filename = "GhibliStudio.log",
    t_list = []
    data = []
    URL = 'https://ghibliapi.herokuapp.com/films'
    # 'https://ghibliapi.herokuapp.com/films'

    try:
        response_data = request_to_response(URL)
        for film_dict_data in response_data:
            for column in film_dict_data:
                if isinstance(film_dict_data[column], list):
                    extracted_data = extract_data(film_dict_data[column], film_dict_data['url'])

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
    format_dict = {}
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
    jsontocsv(dataframe=df, filename="ghibliStudioApi_csv.csv", encoding="utf-8-sig", index=False)
    jsontoexcel(dataframe=df, filename="ghibliStudioApi_xl.xlsx", encoding="utf-8-sig", index=False)
    jsontoxml(dataframe=df, filename="ghibliStudioApi_xml.xml", index=False)
    jsontohtml(dataframe=df, filename="ghibliStudioApi_html.html", escape=False, encoding="utf-8-sig",
               format_dict_arg=format_dict, html_string_arg=html_string, index=False,
               render_links=True, classes="table table-striped table-bordered table-hover table-sm",
               columns=['id', 'title', 'original_title', 'image', 'director', 'producer', 'release_date',
                        'running_time', 'people', 'species', 'locations', 'vehicles'])

    css_path = '.\\df_style.css'
    htmltopdf('ghibliStudioApi_html.html', 'ghibliStudioApi_pdf.pdf', options={"orientation": "Landscape",
                                                                               "page-size": "A3",
                                                                               'user-style-sheet': css_path})
