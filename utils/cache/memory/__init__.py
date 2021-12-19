# ------------------------------
# Functions
# Bake redis key from url params
import json
from datetime import datetime as dt

from utils.cache.interface import ICacheOption

memoryVal = {}

class MemoryCaching(ICacheOption):
    @staticmethod
    def key_params(request) -> str:
        return '.'.join(str(e) for e in request.args.keys())
    # Create new redis key
    @staticmethod
    def create_key(cache_key, val, exp) -> None:
        memoryVal[cache_key] = json.dumps(val)
        memoryVal[cache_key+"-exp"] = exp
        memoryVal[cache_key+"-created"] = dt.now()
    # Get value of key
    @staticmethod
    def get_key(cache_key):
        return memoryVal[cache_key]
    # Check key exist
    @staticmethod
    def exist_key(cache_key) -> bool:
        return memoryVal.get(cache_key) != None and MemoryCaching.cache_expired(cache_key)
    # Expiring memory cache
    @staticmethod
    def cache_expired(cache_key) -> bool:
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
            return False
