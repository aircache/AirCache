import os
from .memory import get_key as memory_get_key, exist_key as memory_exist_key, create_key as memory_create_key, key_params as memory_key_params


config_env = os.environ.get('CACHE_OPTION', 'memory')

if(config_env == "memory"):
    get_key = memory_get_key
    exist_key = memory_exist_key
    create_key = memory_create_key
    key_params = memory_key_params