# Import base packages
from flask import Blueprint, request
from flask.wrappers import Response
import requests
import os
from utils.storage import config_load_headers
from utils.cache import cache_option
from ..middlewares.scope_validator import scope_check
from ..middlewares.api_key_validator import x_api_key
import json
from flask_cors import cross_origin
# ------------------------------
# Blueprint initiation
proxy = Blueprint('proxy', __name__)
# ------------------------------
# Routes
@proxy.route('/<path:text>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@cross_origin()
@x_api_key
@scope_check
def all_routes(text):
    config_data = config_load_headers(request.headers.get("x-api-key"))
    if(request.method.lower() != "options"):
        target_url = config_data['x-target-aircache']
        try:
            redis_key = request.method.lower() + "_"+ request.headers.get("x-api-key") + "_"+ text + "_"+cache_option().key_params(request)
            if(cache_option().exist_key(redis_key+"_content")):
                content_val = cache_option().get_key(redis_key+"_content")
                method_val = cache_option().get_key(redis_key+"_method")
                headers_val = cache_option().get_key(redis_key+"_header")
                headers_list = headers_val[2:-2].split("], [")
                response = Response(json.loads(content_val), method_val)
                for header_obj in headers_list:
                    key_val_pair = header_obj[1:-1].split('", "')
                    response.headers.add(key_val_pair[0], key_val_pair[1])
            else: 
                result = make_request(target_url, config_data)
                expiry_val = config_data['x-api-exp'] or 600
                excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'access-control-allow-origin']
                headers = [(name, value) for (name, value) in result.raw.headers.items()
                    if name.lower() not in excluded_headers]
                if("x-api-cache" in config_data and (result.status_code == 200 or result.status_code == 201 or result.status_code == 202 or result.status_code == 203 or result.status_code == 204)):
                    if(config_data["x-api-cache"] == "true"):
                        if("x-api-cache-options" in config_data):
                            method_options = config_data["x-api-cache-options"].split(',')
                            is_cachable = False
                            for method_item in method_options:
                                if(method_item.replace(" ", "").lower() == request.method.lower()): is_cachable = True
                            if(is_cachable):
                                cache_option().create_key(redis_key+"_content", result.content.decode('utf-8'), expiry_val)
                                cache_option().create_key(redis_key+"_header", headers, expiry_val)
                                cache_option().create_key(redis_key+"_method", result.status_code, expiry_val)
                        else:
                            cache_option().create_key(redis_key+"_content", result.content.decode('utf-8'), expiry_val)
                            cache_option().create_key(redis_key+"_header", headers, expiry_val)
                            cache_option().create_key(redis_key+"_method", result.status_code, expiry_val)
                response = Response(result.content, result.status_code, headers)
            return response
        except Exception:
            return {"error": "somthing went wrong"}, 500
    else:
        return ""

def make_request(target_url, config_data):
    not_allowed_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'access-control-allow-origin', "user-agent", "host"]
    object_dict = dict(zip(config_data["head_key"], config_data["head_value"]))
    copy = {key: value for (key, value) in request.headers if key.lower() not in not_allowed_headers}
    final_headers = {**copy, **object_dict}
    response = requests.request(
        method=request.method,
        url=request.url.replace(os.getenv('HOST'), target_url),
        headers=final_headers,
        data=request.get_data(),
        allow_redirects=False)
    return response
