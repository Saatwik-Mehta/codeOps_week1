import os
import logging
from zipfile import ZipFile

logging.basicConfig(filename='reports.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def zip_file_reports(compressed_file):
    """
    Creates a compressed file of all the files that are present in
    the specified directory.
    :param compressed_file:
    """
    try:
        with ZipFile(compressed_file, 'w') as zipped_folder:
            for folder_name, sub_folders, file_names in os.walk('Generated_reports/GhibliStudio'):
                for file_name in file_names:
                    # create complete filepath of file in directory
                    file_path = os.path.join(folder_name, file_name)
                    # Add file to zip
                    zipped_folder.write(file_path, os.path.basename(file_path))
    except FileNotFoundError as fnf_err:
        logging.exception('No file exists %s', fnf_err)


if __name__ == '__main__':
    zip_file_reports('Ghibli_reports_ankitacode.zip')