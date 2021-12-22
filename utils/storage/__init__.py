import os

from utils.storage.interface import IStorageOption
from .file import FileStorage
from .env_base64 import EnvStorage

config_env = os.environ.get('STORAGE_OPTION', 'file')


def storage_option() -> IStorageOption:
    if(config_env == "file"):
        return FileStorage
    elif(config_env == "env"):
        return EnvStorage
