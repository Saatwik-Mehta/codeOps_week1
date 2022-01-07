## APIDATAHANDLER
This project is created to help users fetch data out of API with specific URL type,
such as, www.exampple.com/objectID, www.exampple2.com/objectID with range [0-9], 
www.exampple.com/somedata. The data retrieved(should be in JSON format) can be used to
to generate the reports in `[*.json, *.html, *.pdf, *.xml, *.xlsx]` format. 

### Example Code:

* To fetch the data out of the API  
```python
from apidatahandler import ApiDataHandler

    URL = 'https://ghibliapi.herokuapp.com/films'

    try:
        object_to_fetch_data = ApiDataHandler(URL)
        response_data = object_to_fetch_data.request_to_response()
    except TypeError as te:
        logging.error('%s: %s', {te.__class__.__name__}, {te})
        sys.exit(1)
    except json.JSONDecodeError as jde:
        logging.error('%s: %s', jde.__class__.__name__, jde)
        sys.exit(1)
    except KeyError as key_err:
        logging.error('%s: %s', key_err.__class__.__name__, key_err)
```
* To generate the reports from Json data
```python
 object_to_fetch_data.json_to_sheets(json_data=data, file_format='csv',
                                            filename=rel_path + 'filename.csv',
                                            encoding='utf-8', index=False)
 object_to_fetch_data.json_to_sheets(json_data=data, file_format='excel',
                                            filename=rel_path + 'filename.xlsx',
                                            encoding='utf-8', index=False)
 object_to_fetch_data.json_to_sheets(json_data=data, file_format='xml',
                                            filename=rel_path + 'filename.xml',
                                            encoding='utf-8', index=False)
 object_to_fetch_data.json_to_html(json_data=data,
                                          filename=rel_path + 'ghibliStudioApi_raw_html.html',
                                          index=False, render_links=False, encoding='utf-8',
                                          columns=['id', 'title', 'original_title',
                                                   'image', 'director', 'producer', 'release_date',
                                                   'running_time', 'people', 'species',
                                                   'locations', 'vehicles'])
 object_to_fetch_data.htmltopdf(html_file=rel_path + 'ghibliStudioApi_raw_html.html',
                                       pdf_file=rel_path + 'ghibliStudioApi_raw_pdf_match.pdf',
                                       options={'orientation': 'Landscape', 'page-size': 'A3'})

```

<br>All the Python files are stored inside the `python_file` folder for easy interaction.
<br>For more info please check [apidatahandler](python_files/apidatahandler.py) file.


