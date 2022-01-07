"""
This module converts the list of files into zipped files and
if given the zipped file it will extract the files into a folder.
"""
import logging
import zipfile

logging.basicConfig(filename='./logs/zip_unzip_files.log', level=logging.INFO,
                    format='%(asctime)s: %(levelname)s:'
                           ' %(filename)s->'
                           ' %(funcName)s->'
                           ' Line %(lineno)d-> %(message)s')


def zip_files(zipped_file_name="zipped_file.zip",
              compress_type=zipfile.ZIP_DEFLATED,
              files_to_zip: list = None):
    """
    This module converts a list of exisitng files into a compressed zip file.
    It used python's inbuilt zipfile module to create the zip file.
    :param zipped_file_name: Name of the zipped file which will contain the compressed files.
    :param compress_type: ZIP_STORED (no compression),
                         ZIP_DEFLATED (requires zlib),
                        ZIP_BZIP2 (requires bz2),
                        ZIP_LZMA (requires lzma).
                        Read zipfile module documentation!
    :param files_to_zip: list of files to zip.
    :return: msg->"Successfully created!"
    """
    try:
        with zipfile.ZipFile(zipped_file_name, 'w') as zipped_file:
            for file in files_to_zip:
                zipped_file.write(file)

        return "Successfully created!"
    except TypeError as type_err:
        logging.error("%s: %s", type_err.__class__.__name__, type_err)
    except AttributeError as att_err:
        logging.error("%s: %s", att_err.__class__.__name__, att_err)
    except FileNotFoundError as file_err:
        logging.error("%s: %s", file_err.__class__.__name__, file_err)
    except Exception as exc:
        logging.error("%s: %s", exc.__class__.__name__, exc)


def unzip_files(zipped_file_name, path="Extracted_folder"):
    """
    This module converts the zipped file into extracted folder with the files inside it.
    :param zipped_file_name: Name of the zipped file that needs to be uncompressed.
    :param path: Name of the extracted folder user wants
    :return: msg-> successfully extracted
    """
    try:
        zip_obj = zipfile.ZipFile(zipped_file_name, 'r')
        zip_obj.extractall(path=path)
        zip_obj.close()
        return "successfully extracted"
    except FileNotFoundError as file_err:
        logging.error("%s: %s", file_err.__class__.__name__, file_err)
    except Exception as exc:
        logging.error("%s: %s", exc.__class__.__name__, exc)


if __name__ == '__main__':
    rel_dir = '../Generated_reports/GhibliStudio/'

    files_to_zip = [rel_dir + 'ghibliStudioApi_csv.csv',
                    rel_dir + 'ghibliStudioApi_html.html',
                    rel_dir + 'ghibliStudioApi_pdf.pdf',
                    rel_dir + 'ghibliStudioApi_xl.xlsx',
                    rel_dir + 'ghibliStudioApi_xml.xml']

    zip_files(zipped_file_name="Generated_reports.zip",
              files_to_zip=files_to_zip)

    # unzip_files(zipped_file_name="Generated_reports.zip", path="../extracted_reports")
