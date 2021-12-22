import json
import os
import re
import base64
from flask import request
from utils.cache import cache_option
from utils.storage.interface import IStorageOption

exp_conf = os.environ.get('EXP_CONF', 10)
config_env = os.environ.get('STORAGE_OPTION', 'file')
if(config_env == "env"):
    exp_conf = os.environ.get('API_CONF')


class EnvStorage(IStorageOption):
    @staticmethod
    def config_load_headers(x_api_key):
        data = EnvStorage.get_data_from_file(x_api_key)
        if(EnvStorage.config_has_api(x_api_key)):
            return data[x_api_key]
        return ""

    @staticmethod
    def config_has_api(x_api_key):
        return x_api_key in EnvStorage.get_data_from_file(x_api_key)

    @staticmethod
    def config_is_scoped(api_key, path):
        data = EnvStorage.get_data_from_file(api_key)
        correct_scope = False
        if(EnvStorage.config_has_api(api_key)):
            for scope in data[api_key]["scopes"]:
                scope_ops = scope.split(" ")
                if(len(scope_ops) > 1):
                    if re.search(scope_ops[1], path) and request.method.lower() == scope_ops[0].lower():
                        correct_scope = True
                elif(len(scope_ops) == 1):
                    if re.search(scope_ops[0], path):
                        correct_scope = True
            return correct_scope
        return False

    @staticmethod
    def get_data_from_file(x_api_key):
        redis_key = x_api_key
        if(cache_option().exist_key(redis_key)):
            return json.loads(cache_option().get_key(redis_key))
        else:
            # returns JSON object as
            # a dictionary
            data = json.loads(base64.b64decode(os.environ.get(
                'API_CONF')).decode('utf8').replace("'", '"'))
            # Closing file
            cache_option().create_key(redis_key, data, exp_conf)
            return data
