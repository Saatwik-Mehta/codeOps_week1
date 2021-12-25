import json
import unittest
from unittest.mock import patch
import os
import logging

logging.basicConfig(filename='log_unittest.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%('
                           'message)s')

from python_files.apidatahandler import ApiDataHandler


class test_ApiDataHandler(unittest.TestCase):
    try:
        def setUp(self) -> None:
            self.myapi = ApiDataHandler('https://ghibliapi.herokuapp.com/films')

        def test_request_to_response(self):
            json = self.myapi.request_to_response()
            self.assertEqual(self.myapi.result.status_code, 200)

        def tearDown(self) -> None:
            print("teardown")
    except ConnectionError as conn_err:
        logging.error(f"{conn_err.__class__.__name__}:{conn_err}")

    except json.decoder.JSONDecodeError as json_err:
        logging.error(f"{json_err.__class__.__name__}:{json_err}")


class test_myapi(unittest.TestCase):
    def setUp(self) -> None:
        self.mypi = ApiDataHandler()

        self.fake_data = [{"people": "Lusheeta Toel Ul Laputa,Pazu,"
                                     "Captain Dola,Colonel Muska,General"
                                     " Mouro,Uncle Pom,Laputian Robot",
                           "species": "Human",
                           "locations": "Gondoa,Pazu's Mines,Laputa,Tedis",
                           "vehicles": "Air Destroyer Goliath",
                           "url": "https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe"
                           }]
        with open("jsonfiles/GhibliStudio.json", 'r') as file:
            self.data = json.load(file)
        self.flat_data = self.mypi.fetch_nested_link_data(api_data=self.data, data_id='url')

    def test_fetch_nested_link_data(self):
        self.flat_data = self.mypi.fetch_nested_link_data(api_data=self.data, data_id='url')
        self.assertEqual(self.flat_data, self.fake_data)

    def test_mock_function(self):
        with patch('python_files.apidatahandler.ApiDataHandler.fetch_nested_link_data') as myfunction:
            myfunction.return_value = self.fake_data
            myfunction(self.data, data_id='url')
            myfunction.assert_called_with(self.data, data_id='url')
            self.assertEqual(self.flat_data, myfunction(self.data, data_id='url'))

    def tearDown(self) -> None:
        print('teardown')


class test_myapi_reports(unittest.TestCase):
    script_dir = os.path.dirname(__file__)
    rel_path_csv = "online_converted/csvjson.csv"
    rel_path_xml = "online_converted/convertjson.xml"
    rel_path_html = "online_converted/codebeautify.html"
    file_path_csv = os.path.join(script_dir, rel_path_csv)
    file_path_xml = os.path.join(script_dir, rel_path_xml)
    file_path_html = os.path.join(script_dir, rel_path_html)

    def setUp(self) -> None:
        with open("test_reports/Ghiblistudiodata_test.csv", "r", encoding="utf-8-sig") as my_csv:
            self.my_csv_content = my_csv.read()
        with open("test_reports/Ghiblistudiodata_test.xml", "r", encoding="UTF-8") as my_xml:
            self.my_xml_content = my_xml.read()
        with open("test_reports/Ghiblistudio_test.html", "r", encoding="UTF-8") as my_html:
            self.my_html_content = my_html.read()
        self.maxDiff = None

    @unittest.skip
    def test_my_generated_files_csv(self):
        with open(self.file_path_csv, 'r', encoding="utf-8-sig") as online_csv_file:
            self.online_csv_content = online_csv_file.read()
        self.assertEqual(self.my_csv_content, self.online_csv_content)

    @unittest.skip
    def test_my_generated_files_xml(self):
        with open(self.file_path_xml, 'r', encoding="utf-8") as online_xml_file:
            self.online_xml_content = online_xml_file.read()
        self.assertEqual(self.my_xml_content, self.online_xml_content)

    @unittest.skip
    def test_my_generated_files_html(self):
        with open(self.file_path_html, 'r', encoding="utf-8-sig") as online_html_file:
            self.online_html_content = online_html_file.read()
        self.assertEqual(self.my_html_content, self.online_html_content)


if __name__ == "__main__":
    unittest.main()
