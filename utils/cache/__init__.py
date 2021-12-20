import os

from utils.cache.interface import ICacheOption
from .memory import MemoryCaching


config_env = os.environ.get('CACHE_OPTION', 'memory')


def cache_option() -> ICacheOption:
    if(config_env == "memory"):
        return MemoryCaching
