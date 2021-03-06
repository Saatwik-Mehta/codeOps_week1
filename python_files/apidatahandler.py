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

logging.basicConfig(filename='./logs/GhibliStudio.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
import os
from typing import Sequence, List
import re
import sys
import pandas
import requests
from IPython.core.display import HTML, display
import pdfkit


class ApiDataHandler:
    """
    This class is helpful to convert the API data into required file format.

    Attributes:
    :param url: API url to retrieve the data for processing.
    :param start_object_id: It is used to retrieve the data from specific
                            object id (start_object_id) to a specific object id (end_object_id).
    :param end_object_id: It is used to retrieve the data from specific
                          object id (start_object_id) to a specific object id (end_object_id).

    The functions included in this class are helpful in to process the data accordingly.
    We can retrieve the Json data, process the nested link data,
    and generate the file with the specified file format.
    """

    def __init__(self, url: str = None, start_object_id: int = None,
                 end_object_id: int = None):
        """
        The constructor for the ApiDataHandler class.
        :param url: API url to retrieve the data for processing.
        :param start_object_id: It is used to retrieve the data from specific
                                object id (start_object_id) to a specific object id (end_object_id).
        :param end_object_id: It is used to retrieve the data from specific
                              object id (start_object_id) to a specific object id (end_object_id).
        """
        self.pdf_file = None
        self.filename = None
        self.dataframe = None
        self.result = None
        self.t_list = []
        if isinstance(url, str) and url != '':
            self.url = url
        elif url is None:
            self.url = url
            logging.warning("Please provide a URL to process!")
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
            into JSON format for data processing.

        :param o_id: This parameter uses URL objectId to retrieve specific data out of the API.
                    If, no value is assigned, the default is set to None,
                    and the given url will be used to retrieve data out of the API
        :return: Json data
        """
        if isinstance(self.url, str):
            try:
                # Validating the URL received from the user.
                if re.match(r'^(http)s?://[a-zA-z]+\.'
                            r'[a-z0-9A-Z-@?&/=:_%~+#]+\.'
                            r'[a-zA-z]{2,5}/?'
                            r'([a-zA-Z0-9]?)+/?'
                            r'([-a-zA-z0-9]?)+/?', self.url):
                    # If the api URL contains object ID and user wants to retrieve the data
                    # user wants to retrieve the data between a specific range
                    if self.start_object_id is not None and self.end_object_id is not None:

                        for ob_id in range(self.start_object_id, self.end_object_id):
                            if not self.url.endswith('/'):
                                self.url = self.url + '/'

                            self.result = requests.get(self.url + str(ob_id))
                            self.result.raise_for_status()

                            if self.result is not None and self.result.ok:
                                self.t_list.append(self.result.json())

                            else:
                                logging.warning('value of result is %s', self.result)
                        return self.t_list
                    elif o_id is None:

                        self.result = requests.get(self.url)
                        self.result.raise_for_status()
                    else:
                        if not self.url.endswith('/'):
                            self.url = self.url + '/'
                        self.result = requests.get(self.url + str(o_id))
                        self.result.raise_for_status()
                else:
                    logging.warning('URL schema is not proper!')
                    raise requests.exceptions.MissingSchema("URL schema is not proper!")

            except requests.ConnectionError as rce:
                logging.error('%s: %s', {rce.__class__.__name__}, {rce})
                logging.error('Couldn\'t make the connection')
                sys.exit(1)
            except requests.HTTPError as http_err:
                logging.error('%s: %s', http_err.__class__.__name__, http_err)
            except json.decoder.JSONDecodeError as jde:
                logging.error('%s: %s', jde.__class__.__name__, jde)
                sys.exit(1)
            else:
                if self.result is not None and self.result.ok:
                    result_data = self.result.json()
                    return result_data
                else:
                    return logging.warning('value of result is %s', self.result.status_code)

    def fetch_nested_link_data(self, api_data: List[dict] = None, data_id=None):
        """
        This function receives the Json String data-> checks for lists
        sequence that may contain the hyperlinks and then retrieves the
        appropriate data out of the hyperlink json data.

        :param api_data: Receives the API data which contains nested
                         URL lists and returns the Json string with
                         URL data converted appropriately.
        :param data_id: A key in the data dictionary that uniquely
                        identifies the data. This field is required
                        to retrieve data from the URL link.

        The key should contain value that is common in
        both the data dictionary and the URL link data. Eg: In the API data of
        https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe:
        This 'url' field value will also be in the 'film' field of the 'people' data.
        :return: List[dict]
        """
        try:
            if api_data is not None:

                if isinstance(api_data, list):

                    api_data = list(filter(None, api_data))
                    for data_dict in api_data:
                        if isinstance(data_dict, dict):
                            for key in data_dict:
                                if data_dict[key] is not None \
                                        and data_id is not None and \
                                        isinstance(data_dict[key], list):
                                    for item in data_dict[key]:

                                        # Looping through each element of data_dict value
                                        # and validating it as a link
                                        if not re.match(r'^(http)s?://[a-zA-z]+\.'
                                                        r'[a-z0-9A-Z-@?&/=:_%~+#]+\.'
                                                        r'[a-zA-z]{2,5}/?'
                                                        r'([a-zA-Z0-9]?)+/?'
                                                        r'([-a-zA-z0-9]?)+/?', item):
                                            continue
                                        response = requests.get(item)
                                        if response is not None and response.ok:
                                            item_data = response.json()

                                            # Replacing the hyperlink with
                                            # data field 'name' or 'title'.
                                            if isinstance(item_data, dict):
                                                data_dict[key][data_dict[key].index(item)] = item_data['name'] \
                                                    if 'name' in item_data else item_data['title'] \
                                                    if 'title' in item_data else ''

                                            elif isinstance(item_data, list):
                                                self.t_list.extend([item_data_dict['name']
                                                                    for item_data_dict in item_data
                                                                    if 'films' in item_data_dict
                                                                    if data_dict[data_id] in
                                                                    item_data_dict['films']])

                                                data_dict[key] = self.t_list
                                                self.t_list = []
                                        else:
                                            logging.warning(f"response from server is {response}")
                                            return None
                                    data_dict[key] = (','.join(data_dict[key])
                                                      if data_dict[key] is not None else '')
                else:
                    logging.error("Expected List of dict! received something else")
                    raise TypeError("Expected List of dict! received something else")
            else:
                logging.warning('No data provided! in flat_list_data function')
                sys.exit(1)
            return api_data
        except requests.ConnectionError as conn_err:
            logging.error('%s: %s', {conn_err.__class__.__name__}, {conn_err})
            logging.info('Connection Interruption while execution')
            sys.exit(1)
        except json.decoder.JSONDecodeError as json_dcd_err:
            logging.error('%s: %s', {json_dcd_err.__class__.__name__}, {json_dcd_err})
            sys.exit(1)

    def json_to_sheets(self, json_data=None, file_format='csv',
                       filename=None, encoding='utf-8', index=False):
        """
        Converts the JSON data fetched from API into
        Excel, Csv, Xml format and saves it inside the file (filename).

        :param json_data: Json data that needs to be converted into available formats.
        :param file_format: The desired file format you wants to convert data into.
                            -> file_format = 'csv' - will convert it into
                                                     csv format(default format),
                            -> file_format = 'excel' - will convert it into Excel format,
                            -> file_format = 'xml' - will convert it into xml format.
        :param filename: User defined filename to save the converted data.
                         It can contain path with filename as well.
                         If no filename is provided, then default filename will be used.
        :param encoding: The encoding value user wants to encode the file data.
        :param index: If each row should include index, default is False.
        :return: None
        """
        try:
            if file_format in ['csv', 'excel', 'xml']:
                if json_data is not None \
                        and (isinstance(json_data, list)
                             or isinstance(json_data, dict)):
                    self.dataframe = pandas.json_normalize(json_data)
                    if not self.dataframe.empty:
                        if file_format.lower() == 'csv':
                            self.filename = 'jsonToCsv.csv' if filename is None else filename
                            self.dataframe.to_csv(self.filename, encoding=encoding, index=index)

                        elif file_format.lower() == 'excel':
                            self.filename = 'jsonToExcel.xlsx' if filename is None else filename
                            self.dataframe.to_excel(self.filename, encoding=encoding, index=index)

                        elif file_format.lower() == 'xml':
                            self.filename = 'jsonToXml.xml' if filename is None else filename
                            self.dataframe.to_xml(self.filename, encoding=encoding, index=index)

                    else:
                        logging.warning("Generated dataFrame is Empty")
                else:
                    logging.error("Given data is not valid!")
            else:
                logging.error(f"file format {file_format} not valid")
        except PermissionError as perm_err:
            logging.error('%s: %s', {perm_err.__class__.__name__}, {perm_err})
            logging.error('Cannot edit the file %s', filename)
            sys.exit(1)

    def json_to_html(self, json_data=None, filename=None, encoding='utf-8', index=False,
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
            if json_data is not None and (isinstance(json_data, list) or isinstance(json_data, dict)):
                self.dataframe = pandas.json_normalize(json_data)
                self.filename = 'jsonToHtml.html' if filename is None else filename
                display(HTML(self.dataframe.to_html(escape=False, formatters=format_dict_arg)))
                if html_string_arg is not None:
                    with open(filename, mode='w', encoding=encoding) as file:
                        file.write(html_string_arg.format(table=self.dataframe.to_html(index=index,
                                                                                       escape=escape,
                                                                                       formatters=format_dict_arg,
                                                                                       render_links=render_links,
                                                                                       classes=classes,
                                                                                       columns=columns)))
                else:
                    self.dataframe.to_html(filename, index=index,
                                           escape=escape,
                                           render_links=render_links,
                                           classes=classes, columns=columns, encoding=encoding)
        except PermissionError as perm_err:
            logging.error('%s: %s', {perm_err.__class__.__name__}, {perm_err})
            logging.error('Cannot edit the file %s', filename)
            sys.exit(1)

    def htmltopdf(self, html_file, pdf_file, pathto_wkhtmltopdf=None, options=None, css=None):
        """
        Uses pdfkit library to convert the HTML file into PDF file.

        :param html_file: Path to the HTML file from which PDF file will be generated
        :param pdf_file: User defined filename to save the converted data.
                         It can contain path with filename as well.
        :param pathto_wkhtmltopdf: path to wkhtmltopdf folder[if required].
        :param options: a dict object to format the pdf file.
        :param css: css file name to be used in pdf file.
                    Path can also be included (if required).
        :return: None
        """
        try:
            if os.path.splitext(html_file)[-1] == '.html' and os.path.isfile(html_file):
                self.pdf_file = 'apidatapdf.pdf' if pdf_file is None else pdf_file
                config = pdfkit.configuration(wkhtmltopdf=pathto_wkhtmltopdf)
                pdfkit.from_file(html_file, pdf_file,
                                 configuration=config, options=options, css=css)
            else:
                logging.warning('No such file %s', html_file, 'exists!')

        except PermissionError as perm_err:
            logging.error('%s: %s', {perm_err.__class__.__name__}, {perm_err})
            logging.error('Cannot edit the file %s', pdf_file)
            sys.exit(1)
