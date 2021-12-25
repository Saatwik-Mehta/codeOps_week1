import json
import logging
from pathlib import Path

logs_dir = '/logs/'
Path(logs_dir).mkdir(exist_ok=True)
logging.basicConfig(filename="."+logs_dir+"Colleagues.log", level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

from apidatahandler import ApiDataHandler

try:
    obj = ApiDataHandler()
    with open('../jsonfiles/crypto_ap_url.json', 'r') as json_file:
        json_data = json.load(json_file)
    report_dir = '../Generated_reports/crypto_Api_Url/'
    Path(report_dir).mkdir(parents=True, exist_ok=True)
    obj.json_to_sheets(json_data=json_data, file_format='csv',
                       filename=report_dir + 'crypto_api_url.csv',
                       encoding='utf-8', index=False)

except PermissionError as perm_err:
    logging.error('%s: %s', perm_err.__class__.__name__, perm_err)
except ConnectionError as conn_err:
    logging.error("%s: %s", conn_err.__class__.__name__, conn_err)
except FileNotFoundError as file_err:
    logging.error("%s: %s", file_err.__class__.__name__, file_err)
