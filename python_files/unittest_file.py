import json
import unittest
from unittest.mock import patch
import pandas
import os
import logging
import hashlib

import requests

logging.basicConfig(filename='./logs/log_unittest.log',
                    level=logging.INFO,
                    format='%(asctime)s: %(levelname)s:'
                           ' %(filename)s->'
                           ' %(funcName)s->'
                           ' Line %(lineno)d-> %(message)s')

from apidatahandler import ApiDataHandler


class test_ApiDataHandler(unittest.TestCase):
    try:
        def setUp(self) -> None:
            with open("../test_reports/StudioGhibliApi_raw.json",
                      'r', encoding='utf-8') as my_json:
                self.json_content = json.load(my_json)
            with open("../test_reports/brokenJson.json", "r", encoding="utf-8") as json_file:
                self.jsondata = json_file.read()
            self.myapi = ApiDataHandler('https://ghibliapi.herkuapp.com/films')

        def test_url(self):
            self.assertRaises(json.decoder.JSONDecodeError, self.myapi.request_to_response)

        def test_url_struc(self):
            self.myapi.url = '355654'
            self.assertRaises(requests.exceptions.MissingSchema
                              , self.myapi.request_to_response
                              )

        @patch('apidatahandler.ApiDataHandler.request_to_response')
        def test_mock_api_struct(self, mock_func):
            mock_func.side_effect = requests.exceptions.MissingSchema
            self.myapi.url = '355654'
            with self.assertRaises(requests.exceptions.MissingSchema):
                self.myapi.request_to_response()

        @patch('apidatahandler.requests.get')
        def test_mock_api_HTTP(self, mock_get):
            mock_get.return_value.status_code = 404
            mock_get.side_effect = requests.exceptions.HTTPError
            with self.assertRaises(requests.exceptions.HTTPError):
                self.myapi.request_to_response()

        @patch('apidatahandler.requests.get')
        def test_mock_response_ok(self, mock_get):
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = self.json_content
            d = self.myapi.request_to_response()
            self.assertIsNotNone(d)

        @patch('apidatahandler.requests.get')
        def test_mock_response_not_ok(self, mock_get):
            mock_get.return_value.ok = False
            d = self.myapi.request_to_response()
            self.assertIsNone(d)

        def tearDown(self) -> None:
            print("teardown")

    except ConnectionError as conn_err:
        logging.error(f"{conn_err.__class__.__name__}:{conn_err}")

    except json.decoder.JSONDecodeError as json_err:
        logging.error(f"{json_err.__class__.__name__}:{json_err}")


class test_myapi(unittest.TestCase):
    def setUp(self) -> None:
        self.mypi = ApiDataHandler()

        with open("../test_reports/Expected.json", 'r', encoding="utf-8") as json_data:
            self.fake_data = json.load(json_data)

        with open("../jsonfiles/GhibliStudio.json", 'r') as file:
            self.data = json.load(file)

    @patch('apidatahandler.requests.get')
    def test_mock_response_not_ok(self, mock_get):
        mock_get.return_value.ok = False
        data_mock = self.mypi.fetch_nested_link_data(api_data=self.data, data_id='url')

        self.assertIsNone(data_mock)

    def test_check_json_data(self):
        with self.assertRaises(TypeError):
            self.mypi.fetch_nested_link_data(api_data=345345432, data_id='url')

    @patch('apidatahandler.ApiDataHandler.fetch_nested_link_data')
    def test_mock_check_json_data(self, mock_func):
        mock_func.side_effect = TypeError
        with self.assertRaises(TypeError):
            self.mypi.fetch_nested_link_data(api_data=345345432, data_id='url')

    def tearDown(self) -> None:
        print('teardown')


class test_converter_func(unittest.TestCase):
    def setUp(self) -> None:
        self.mypi = ApiDataHandler()

    def test_json_to_sheets(self):
        self.mypi.json_to_sheets(json_data=['12345', '3456erwr'], file_format='csv',
                                 filename=None, encoding='utf-8', index=False)


class test_myapi_reports(unittest.TestCase):
    script_dir = os.path.dirname(__file__)

    rel_path_json = "../Truth_Folder/jsonfiles/StudioGhibliApi.json"
    rel_path_csv = "../Truth_Folder/GhibliStudio/ghibliStudioApi_csv.csv"
    rel_path_xml = "../Truth_Folder/GhibliStudio/ghibliStudioApi_xml.xml"
    rel_path_html = "../Truth_Folder/GhibliStudio/ghibliStudioApi_html.html"
    rel_path_xl = "../Truth_Folder/GhibliStudio/ghibliStudioApi_xl.xlsx"
    rel_path_pdf = "../Truth_Folder/GhibliStudio/ghibliStudioApi_raw_pdf_2.pdf"

    file_path_csv = os.path.join(script_dir, rel_path_csv)
    file_path_json = os.path.join(script_dir, rel_path_json)
    file_path_xml = os.path.join(script_dir, rel_path_xml)
    file_path_html = os.path.join(script_dir, rel_path_html)
    file_path_xl = os.path.join(script_dir, rel_path_xl)
    file_path_pdf = os.path.join(script_dir, rel_path_pdf)

    def setUp(self) -> None:
        with open("../test_reports/GhibliStudio/ghibliStudioApi_csv.csv", "r", encoding="utf-8-sig") as my_csv:
            self.my_csv_content = my_csv.read()

        with open("../test_reports/GhibliStudio/ghibliStudioApi_xml.xml", "r", encoding="UTF-8") as my_xml:
            self.my_xml_content = my_xml.read()
        with open("../test_reports/GhibliStudio/ghibliStudioApi_html.html", "r", encoding="UTF-8-SIG") as my_html:
            self.my_html_content = my_html.read()
        with open("../test_reports/StudioGhibliApi.json", "r", encoding='utf-8') as my_json:
            self.my_json_content = json.load(my_json)
        with open("../test_reports/GhibliStudio/ghibliStudioApi_xl.xlsx", "rb") as my_xl:
            self.my_xl_content = my_xl.read()
        self.my_xl_df = pandas.read_excel("../test_reports/GhibliStudio/ghibliStudioApi_xl.xlsx")
        self.my_pdf_md5 = hashlib.md5(open('../test_reports/GhibliStudio/ghibliStudioApi_raw_pdf_match.pdf',
                                           'rb').read()).hexdigest()
        with open('../test_reports/GhibliStudio/ghibliStudioApi_raw_pdf_2.pdf', 'rb') as pdf_file2:
            self.test_cont = pdf_file2.read()
        self.maxDiff = None

    def test_my_generated_files_csv(self):
        with open(self.file_path_csv, 'r', encoding="utf-8-sig") as truth_csv_file:
            self.truth_csv_content = truth_csv_file.read()
        self.assertEqual(self.my_csv_content, self.truth_csv_content)

    def test_my_generated_files_xml(self):
        with open(self.file_path_xml, 'r', encoding="utf-8") as truth_xml_file:
            self.truth_xml_content = truth_xml_file.read()
        self.assertEqual(self.my_xml_content, self.truth_xml_content)

    def test_my_generated_files_html(self):
        with open(self.file_path_html, 'r', encoding="utf-8-sig") as truth_html_file:
            self.truth_html_content = truth_html_file.read()
        self.assertEqual(self.my_html_content, self.truth_html_content)

    def test_my_generated_files_xl(self):
        self.truth_xl_df = pandas.read_excel(self.file_path_xl)
        print("excel comp:\n", self.my_xl_df.compare(self.truth_xl_df))

    def test_my_generated_files_json(self):
        with open(self.file_path_json, 'r', encoding='utf-8') as truth_json_file:
            self.truth_json_content = json.load(truth_json_file)
        self.assertEqual(self.my_json_content, self.truth_json_content)

    def test_my_generated_files_pdf(self):
        self.truth_pdf_md5 = hashlib.md5(open('../test_reports/GhibliStudio/ghibliStudioApi_raw_pdf_match2.pdf',
                                              'rb').read()).hexdigest()
        self.assertEqual(self.my_pdf_md5, self.truth_pdf_md5)

    def test_my_generated_files_pdf_comp(self):
        with open(self.file_path_pdf, 'rb') as pdf_file:
            self.truth_cont = pdf_file.read()
        self.assertEqual(self.truth_cont, self.test_cont)


if __name__ == "__main__":
    unittest.main()
