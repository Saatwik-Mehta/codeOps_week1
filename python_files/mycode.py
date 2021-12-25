from apidatahandler import ApiDataHandler
import logging
logging.basicConfig(filename='../GhibliStudio.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%('
                           'message)s')
try:
    obj = ApiDataHandler("https://ghibliapi.herokuapp.com/films")
    my_data = obj.request_to_response()
    obj.json_to_html(my_data, "Ghiblistudio_test.html", "utf-8-sig", render_links=False)

except ConnectionError as conn_err:
    logging.error(f"{conn_err.__class__.__name__}: {conn_err}")