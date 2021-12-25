import logging
import pandas
import pathlib

logging.basicConfig(filename='./logs/Metropolitan_museum_api.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%('
                           'message)s')

from apidatahandler import ApiDataHandler

URL = 'https://collectionapi.metmuseum.org/public/collection/v1/objects'


def get_list_col_func(api_data=None):
    get_list_col = []
    remove_col = []
    if api_data is not None:
        if isinstance(api_data, list):
            get_list_col = [key for data_dict in api_data
                            for key in data_dict if isinstance(data_dict[key], list)
                            and key not in get_list_col]
            get_list_col = list(set(get_list_col))
            for dict_data in api_data:
                for key in get_list_col:
                    if dict_data[key] is not None and dict_data[key] != []:
                        if isinstance(dict_data[key][0], dict):
                            continue
                        remove_col.append(key)
                        dict_data[key] = ''.join(dict_data[key])
        get_list_col = [i for i in get_list_col if i not in remove_col]
    return get_list_col


def flat_data(api_data=None, nested_data_col=None):
    if nested_data_col is not None and api_data:
        api_data_df = pandas.DataFrame(api_data)
        for column in nested_data_col:
            dataframe = pandas.json_normalize(api_data, record_path=column, record_prefix=column + '_')
            for col in dataframe:
                api_data_df[col] = dataframe[col]
            api_data_df = api_data_df.drop(columns=[column], axis=1)

    return api_data_df


try:
    object_d = ApiDataHandler(URL, 1, 50)
    response_data = object_d.request_to_response()
    nested_col = get_list_col_func(api_data=response_data)
    data = flat_data(response_data, nested_col)
    rel_dir = '../Generated_reports/Metropolitan_museum/'
    pathlib.Path(rel_dir).mkdir(exist_ok=True)
    data.to_csv(rel_dir + 'Metropolitan_Museum_api.csv', index=False)
except Exception as e:
    print(e)
