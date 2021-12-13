"""
This module helps to convert the API data, with nested links containing web url,
into these respective format (CSV, EXCEL, PDF, HTML, XML). The functions included in
this module includes
1. request_to_response - method()
2. fetch_nested_link_data - method()
3. jsonconverter - method()
4. htmltopdf - method().
"""
import json
import logging
import os
from typing import Sequence, List
import re
import pandas
import requests
import sys
import validator
from IPython.core.display import HTML, display
import pdfkit

logging.basicConfig(filename="GhibliStudio.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%("
                                                                            "message)s")


class ApiDataHandler:
    """
    This class is helpful to convert the API data into required file format.

    Attributes:
    :param url: API url to retrieve the data for processing.
    :param start_object_id: It is used to retrieve the data from specific object id (start_object_id)
                          to a specific object id (end_object_id).
    :param end_object_id: It is used to retrieve the data from specific object id (start_object_id)
                          to a specific object id (end_object_id).

    The functions included in this class are helpful in to process the data accordingly.
    We can retrieve the Json data, process the nested link data, and generate the file with the specified file format.
    """

    def __init__(self, url: str = '', start_object_id: int = None,
                 end_object_id: int = None):
        """
        The constructor for the ApiDataHandler class.
        :param url: API url to retrieve the data for processing.
        :param start_object_id: It is used to retrieve the data from specific object id (start_object_id)
                          to a specific object id (end_object_id).
        :param end_object_id: It is used to retrieve the data from specific object id (start_object_id)
                          to a specific object id (end_object_id).
        """
        self.pdf_file = None
        self.filename = None
        self.dataframe = None
        self.result = None
        self.t_list = []
        if isinstance(url, str) and len(url):
            self.url = url
        if isinstance(start_object_id, int):
            self.start_object_id = start_object_id
        else:
            self.start_object_id = None
        if isinstance(end_object_id, int):
            self.end_object_id = end_object_id
        else:
            self.end_object_id = None

    def request_to_response(self, o_id: str = None):
        """
           This function is used to convert the requested API data
            into JSON String format for data processing.

        :param o_id: This parameter uses URL objectId to retrieve specific data out of the API.
                    If, no value is assigned, the default is set to None, and the given url will be used
                    to retrieve data out of the API
        :return: JSON string
        """
        if isinstance(self.url, str):
            try:
                # validating the URL received from the user.
                if re.match(r"^(http)s?://[a-zA-z]+\.[a-z0-9A-Z-@?&/=:_%~+#]+\.[a-zA-z]{2,"
                            r"5}/?([a-zA-Z0-9]?)+/?([-a-zA-z0-9]?)+", self.url):
                    # if the api URL contains object ID and user wants to retrieve the data
                    # user wants to retrieve the data between a specfic range
                    if self.start_object_id is not None and self.end_object_id is not None:

                        for o_id in range(self.start_object_id, self.end_object_id):
                            if not self.url.endswith('/'):
                                self.url = self.url + '/'

                            self.result = requests.get(self.url + str(o_id))

                            if self.result is not None and len(self.result.json()):
                                self.t_list.append(self.result.json())
                                return self.t_list
                            else:
                                logging.warning("value of result is ".format(self.result))
                    elif o_id is None:
                        self.result = requests.get(self.url)
                    else:
                        if not self.url.endswith('/'):
                            self.url = self.url + '/'
                        self.result = requests.get(self.url + str(o_id))
                else:
                    logging.warning("URL schema is not proper!")
                    sys.exit(1)
            except requests.exceptions.MissingSchema as ms:
                logging.error(f"{ms.__class__.__name__}: {ms}")
                sys.exit(1)
            except requests.ConnectionError as rce:
                logging.error(f"{rce.__class__.__name__}: {rce}")
                logging.error("Couldn't make the connection")
                sys.exit(1)
            except json.JSONDecodeError as jde:
                logging.error(f"{jde.__class__.__name__}: {jde}")
                sys.exit(1)

            else:
                if self.result is not None or self.result.json():
                    result_data = self.result.json()
                    return result_data
                else:
                    logging.warning("value of result is ".format(self.result))

    def fetch_nested_link_data(self, api_data: List[dict] = None, data_id=None):
        """
        This function receives the Json String data-> checks for lists sequence that may contain the hyperlinks
        and then retrieves the appropriate data out of the hyperlink json data.
        :param api_data: Receives the API data which contains nested URL lists and returns the Json string with URL
        data converted appropriately.
        :param data_id: A key in the data dictionary that uniquely identifies the data.
        This field is required to retrieve data from the URL link. The key should contain value that is common in
        both the data dictionary and the URL link data. Eg: In the API data of
        https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe:
        This 'url' field value will also be in the 'film' field of the 'people' data.
        :return: List[dict]
        """
        try:
            if api_data is not None:

                if isinstance(api_data, list):

                    api_data = [i for i in filter(None, api_data)]
                    for data_dict in api_data:
                        for key in data_dict:
                            if data_dict[key] is not None \
                                    and data_id is not None and \
                                    isinstance(data_dict[key], list):
                                for item in data_dict[key]:

                                    # looping through each element of dict value and validating it as a link
                                    if not re.match(r"^(http)s?://[a-zA-z]+\.[a-z0-9A-Z-@?&/=:_%~+#]+\.[a-zA-z]{2,"
                                                    r"5}/?([a-zA-Z0-9]?)+/?([-a-zA-z0-9]?)+", item):
                                        continue
                                    response = requests.get(item)
                                    if response is not None and len(response.json()):
                                        item_data = response.json()

                                        # replacing the hyperlink with data field 'name' or 'title'.
                                        if isinstance(item_data, dict):
                                            data_dict[key][data_dict[key].index(item)] = item_data['name'] \
                                                if 'name' in item_data else item_data['title']
                                        elif isinstance(item_data, list):
                                            self.t_list.extend([item_data_dict['name'] for item_data_dict in item_data
                                                                if data_dict[data_id] in item_data_dict['films']])

                                            data_dict[key] = self.t_list
                                            self.t_list = []

                                data_dict[key] = (','.join(data_dict[key]) if data_dict[key] is not None else '')

                elif isinstance(api_data, dict):
                    pass

            else:
                logging.warning("No data provided! in flat_list_data function")
                exit(1)
            return api_data
        except requests.ConnectionError as ae:
            logging.error(f"{ae.__class__.__name__}: {ae}")
            logging.info("Connection Interruption while execution")
            sys.exit(1)
        except TypeError as te:
            logging.error(f"{te.__class__.__name__}:{te}")
            sys.exit(1)
        except json.JSONDecodeError as jde:
            logging.error(f"{jde.__class__.__name__}: {jde}")
            sys.exit(1)

    def jsontosheets(self, json_data=None, file_format='csv', filename=None, encoding="utf-8", index=False):
        """
        Converts the JSON data fetched from API into
        Excel, Csv, Xml format and saves it inside the file (filename).
        :param json_data: Json data that needs to be converted into available formats.
        :param file_format: The desired file format you wants to convert data into.
                            -> file_format = 'csv' - will convert it into csv format(default format),
                            -> file_format = 'excel' - will convert it into Excel format,
                            -> file_format = 'xml' - will convert it into xml format.
        :param filename: User defined filename to save the converted data. It can contain path with filename as well.
                         If no filename is provided, then default filename will be used.
        :param encoding: The encoding value user wants to encode the file data.
        :param index: If each row should include index, default is False.
        :return: None
        """
        try:
            if json_data is not None and len(json_data):
                self.dataframe = pandas.DataFrame(json_data)

                if file_format.lower() == 'csv':
                    self.filename = "jsonToCsv.csv" if filename is None else filename
                    self.dataframe.to_csv(self.filename, encoding=encoding, index=index)

                elif file_format.lower() == 'excel':
                    self.filename = "jsonToExcel.xlsx" if filename is None else filename
                    self.dataframe.to_excel(self.filename, encoding=encoding, index=index)

                elif file_format.lower() == 'xml':
                    self.filename = "jsonToXml.xml" if filename is None else filename
                    self.dataframe.to_xml(self.filename, encoding=encoding, index=index)

            else:
                logging.warning(f"file format {file_format} not allowed!")
        except PermissionError as pe:
            logging.error(f"{pe.__class__.__name__}: {pe}")
            logging.error(f"Cannot edit the file {filename}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"{e.__class__.__name__}:{e}")

    def jsontohtml(self, json_data=None, filename=None, encoding="utf-8", index=False,
                   escape=False, format_dict_arg=None, html_string_arg=None, render_links=True,
                   classes: str = None, columns: Sequence[str] = None):
        """
        This method generates the HTML file from JSON data retrieved from API.
        User can give desire HTML formatting to represent the data in the browser.
        If not, then a simple table will be generated using HTML table tags in the file.

        :param json_data: Json data that needs to be converted into available formats
        :param filename: User defined filename to save the converted data.
                         It can contain path with filename as well.
                         If, no filename is provided, then default filename will be used.
        :param encoding: The encoding value user wants to encode the file data.
        :param index: If each row should include index, default is False.
        :param escape: Convert the characters <, >, and & to HTML-safe sequences.
        :param format_dict_arg: formatters for HTML elements
        :param html_string_arg: HTML template for the data presentation.
        :param render_links: renders the document URL links to HTML hyperlink
        :param classes: Add classes to HTML template
        :param columns: Data Columns for include in HTML file
        :return: None
        """
        try:
            if json_data is not None and len(json_data):
                self.dataframe = pandas.DataFrame(json_data)
                self.filename = "jsonToHtml.html" if filename is None else filename
                display(HTML(self.dataframe.to_html(escape=False, formatters=format_dict_arg)))
                if html_string_arg is not None:
                    with open(filename, mode="w", encoding=encoding) as f:
                        f.write(html_string_arg.format(table=self.dataframe.to_html(index=index, escape=escape,
                                                                                    formatters=format_dict_arg,
                                                                                    render_links=render_links,
                                                                                    classes=classes,
                                                                                    columns=columns)))
                else:
                    self.dataframe.to_html(filename, index=index, escape=escape,
                                           render_links=render_links, classes=classes, columns=columns)
        except PermissionError as pe:
            logging.error(f"{pe.__class__.__name__}: {pe}")
            logging.error(f"Cannot edit the file {filename}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"{e.__class__.__name__}:{e}")

    def htmltopdf(self, html_file, pdf_file, pathto_wkhtmltopdf=None, options=None, css=None):
        """
        Uses pdfkit library to convert the HTML file into PDF file.

        :param html_file: Path to the HTML file from which PDF file will be generated
        :param pdf_file: User defined filename to save the converted data. It can contain path with filename as well.
        :param pathto_wkhtmltopdf: path to wkhtmltopdf folder[if required].
        :param options: a dict object to format the pdf file.
        :param css: css file name to be used in pdf file. Path can also be included (if required).
        :return: None
        """
        try:
            if os.path.splitext(html_file)[-1].lower() == '.html' and os.path.isfile(html_file):
                self.pdf_file = 'apidatapdf.pdf' if pdf_file is None else pdf_file
                config = pdfkit.configuration(wkhtmltopdf=pathto_wkhtmltopdf)
                pdfkit.from_file(html_file, pdf_file, configuration=config, options=options, css=css)
            else:
                logging.warning(f"No such file {html_file} exists!")

        except PermissionError as pe:
            logging.error(f"{pe.__class__.__name__}: {pe}")
            logging.error(f"Cannot edit the file {pdf_file}")
            sys.exit(1)
