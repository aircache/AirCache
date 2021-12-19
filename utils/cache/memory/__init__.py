# ------------------------------
# Functions
# Bake redis key from url params
import json
from datetime import datetime as dt

memoryVal = {}

def key_params(request):
    return '.'.join(str(e) for e in request.args.keys())
# Create new redis key
def create_key(cache_key, val, exp):
    memoryVal[cache_key] = json.dumps(val)
    memoryVal[cache_key+"-exp"] = exp
    memoryVal[cache_key+"-created"] = dt.now()
# Get value of key
def get_key(cache_key):
    return memoryVal[cache_key]
# Check key exist
def exist_key(cache_key):
    return memoryVal.get(cache_key) != None and cache_expired(cache_key)
# Expiring memory cache
def cache_expired(cache_key):
    exp = memoryVal[cache_key+"-exp"]
    difference = (dt.now() - memoryVal[cache_key+"-created"])
    total_seconds = difference.total_seconds()
    try:
        if(total_seconds > float(exp)):
            memoryVal.pop(cache_key)
            memoryVal.pop(cache_key+"-exp")
            memoryVal.pop(cache_key+"-created")
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False
