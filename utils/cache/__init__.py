import os

from utils.cache.interface import ICacheOption
from utils.cache.redis import RedisCaching
from .memory import MemoryCaching

from dotenv import load_dotenv

load_dotenv()

config_env = os.environ.get('CACHE_OPTION', 'memory')

def cache_option() -> ICacheOption:
    if(config_env == "memory"):
        return MemoryCaching
    elif(config_env == "redis"):
        return RedisCaching
