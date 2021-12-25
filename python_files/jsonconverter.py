import pandas
import logging
from typing import Sequence
from IPython.core.display import display, HTML

logging.basicConfig(filename="../GhibliStudio.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%("
                                                                            "message)s")


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
                                                                       formatters=format_dict_arg,
                                                                       render_links=render_links,
                                                                       classes=classes,
                                                                       columns=columns)))
        except PermissionError as pe:
            logging.error(f"{pe.__class__.__name__}: {pe}")
            logging.info(f"Cannot edit the file {filename}")
