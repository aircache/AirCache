# Import base packages
import redis
import json
import os
# ------------------------------
# Redis configuration
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
# ------------------------------
# Functions
# Bake redis key from url params


def redis_key_params(request) -> str:
    return '.'.join(str(e) for e in request.args.keys())
# Create new redis key


def create_key(redis_key, val, exp) -> None:
    r_connection.setex(redis_key, int(exp), json.dumps(val))
# Get value of key


def get_key(redis_key):
    return r_connection.get(redis_key)
# Check key exist


def exist_key(redis_key):
    return r_connection.exists(redis_key)
