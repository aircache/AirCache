from flask import request
from functools import wraps

from utils.storage import storage_option
# rapid api secret validator

# !!! Developer comment, this should get the config not from .env directly


def x_api_key(func):
    @wraps(func)
    def check(*args, **kwargs):
        if(request.method != "OPTIONS"):
            if(storage_option().config_has_api(request.headers.get('x-api-key'))):
                return func(*args, **kwargs)
            else:
                return {"error": "forbidden"}, 401
        else:
            return func(*args, **kwargs)
    return check
