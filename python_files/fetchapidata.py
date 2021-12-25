import requests
import logging
import sys

logging.basicConfig(filename="../GhibliStudio.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%("
                                                                            "message)s")


def request_to_response(api_url: str):
    """
    This function is used to convert the requested API data
    into JSON format for data processing

    :param api_url: This parameter takes the website URL in string format
                    eg: "http://somesiteapi.com/somedatatofetch?"
    :return: Returning data will be in Json format for data processing.
    """
    if isinstance(api_url, str) and len(str):
        try:
            result = requests.get(api_url)
        except requests.exceptions.MissingSchema as ms:
            logging.error(f"{ms.__class__.__name__}: {ms}")
            sys.exit(1)
        except requests.ConnectionError as rce:
            logging.error(f"{rce.__class__.__name__}: {rce}")
            logging.info("Couldn't make the connection")
            sys.exit(1)
        else:
            result_data = result.json()
            return result_data
