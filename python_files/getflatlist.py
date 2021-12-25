import logging
import requests

logging.basicConfig(filename="../GhibliStudio.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%("
                                                                            "message)s")


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

    t_list = []
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
