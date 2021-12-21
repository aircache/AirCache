# Import base packages
from utils.cache.interface import ICacheOption
from datetime import datetime as dt
import redis
import json
import os

from dotenv import load_dotenv

load_dotenv()

# ------------------------------
# Redis configuration
config_env = os.environ.get('CACHE_OPTION', 'memory')
if(config_env == "redis"):
    redis_host = os.environ.get('CACHE_REDIS_HOST', 'localhost')
    redis_port = os.environ.get('CACHE_REDIS_PORT', 6379)
    redis_pass = os.environ.get('CACHE_REDIS_PASSWORD', '')
    redis_user = os.environ.get('CACHE_REDIS_USERNAME', '')
    redis_url = os.environ.get('CACHE_REDIS_URL', '')
    redis_type = os.environ.get('CACHE_REDIS_CONNECTION', 'host')

    if redis_type == 'host':
        r_connection = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_pass,
                                         username=redis_user, ssl=False, charset="utf-8", decode_responses=True)
    elif redis_type == 'url':
        r_connection = redis.StrictRedis.from_url(redis_url)

class RedisCaching(ICacheOption):
    @staticmethod
    def key_params(request) -> str:
        return '.'.join(str(e) for e in request.args.keys())
    # Create new redis key

    @staticmethod
    def create_key(cache_key, val, exp) -> None:
        r_connection.setex(cache_key, int(exp), json.dumps(val))
    # Get value of key

    @staticmethod
    def get_key(cache_key):
        return r_connection.get(cache_key)
    # Check key exist

    @staticmethod
    def exist_key(cache_key) -> bool:
        return r_connection.exists(cache_key)
