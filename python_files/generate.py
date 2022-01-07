import requests
import logging
logging.basicConfig(level=logging.INFO)

def response_fn(URL: None):
    try:
        response = requests.get(URL)

    except requests.exceptions.MissingSchema as miss_sch:
        logging.error(f"{miss_sch}")

