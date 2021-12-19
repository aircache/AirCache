import os
from .file import has_api as file_has_api, load_headers as file_load_headers, is_scoped as file_is_scoped
# from .db import has_api as db_has_api, load_headers as db_load_headers, is_scoped as db_is_scoped

config_env = os.environ.get('STORAGE_OPTION', 'file')

if(config_env == "file"):
    config_has_api = file_has_api
    config_load_headers = file_load_headers
    config_is_scoped = file_is_scoped
'''
elif(config_env == "db"):
    config_has_api = db_has_api
    config_load_headers = db_load_headers
    config_is_scoped = db_is_scoped
'''