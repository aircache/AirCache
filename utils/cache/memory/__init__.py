# ------------------------------
# Functions
# Bake redis key from url params
import json

memoryVal = {}

def key_params(request):
    return '.'.join(str(e) for e in request.args.keys())
# Create new redis key
def create_key(redis_key, val, exp):
    memoryVal[redis_key] = json.dumps(val)
# Get value of key
def get_key(redis_key):
    return memoryVal[redis_key]
# Check key exist
def exist_key(redis_key):
    return memoryVal.get(redis_key) != None