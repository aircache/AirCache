import json
import os
import re
from flask import  request
from utils.cache import cache_option
from utils.storage.interface import IStorageOption

exp_conf = os.environ.get('EXP_CONF', 10)

class FileStorage(IStorageOption):
    @staticmethod
    def config_load_headers(x_api_key):
        data = FileStorage.get_data_from_file(x_api_key)
        if(FileStorage.config_has_api(x_api_key)):
            return data[x_api_key]
        else:
            return ""

    @staticmethod
    def config_has_api(x_api_key):
        return x_api_key in FileStorage.get_data_from_file(x_api_key)

    @staticmethod
    def config_is_scoped(api_key, path):
        data = FileStorage.get_data_from_file(api_key)
        correct_scope = False
        if(FileStorage.config_has_api(api_key)):
            for scope in data[api_key]["scopes"]:
                scope_ops = scope.split(" ")
                if(len(scope_ops) > 1):
                    if re.search(scope_ops[1], path) and request.method.lower() == scope_ops[0].lower(): correct_scope = True
                elif(len(scope_ops) == 1):
                    if re.search(scope_ops[0], path): correct_scope = True
            return correct_scope
        else:
            return False

    @staticmethod
    def get_data_from_file(x_api_key):
        redis_key = x_api_key
        if(cache_option().exist_key(redis_key)):
            return json.loads(cache_option().get_key(redis_key))
        else:
            # Opening JSON file
            f = open('./conf/api.json')
            # returns JSON object as
            # a dictionary
            data = json.load(f)
            # Closing file
            f.close()
            cache_option().create_key(redis_key, data, exp_conf)
            return data

