import json
from flask import request
from functools import wraps
import os
import json

from utils.storage import storage_option
# rapid api secret validator

# !!! Developer comment, this should get the config not from .env directly


def scope_check(func):
    @wraps(func)
    def check(*args, **kwargs):
        if(request.method != "OPTIONS"):
            if(storage_option().config_is_scoped(request.headers.get('x-api-key'), request.full_path)):
                return func(*args, **kwargs)
            else:
                return {"error": "forbidden"}, 401
        else:
            return func(*args, **kwargs)
    return check
