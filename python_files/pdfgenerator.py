import pdfkit
import logging
import os

logging.basicConfig(filename="../GhibliStudio.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%("
                                                                            "message)s")


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
    if os.path.splitext(html_file)[-1].lower() == '.html' and os.path.isfile(html_file):
        try:
            config = pdfkit.configuration(wkhtmltopdf=pathto_wkhtmltopdf)
            pdfkit.from_file(html_file, pdf_file, configuration=config, options=options, css=css)

        except PermissionError as pe:
            logging.error(f"{pe.__class__.__name__}: {pe}")
            logging.error(f"Cannot edit the file {pdf_file}")
