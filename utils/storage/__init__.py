import os

from utils.storage.interface import IStorageOption
from .file import FileStorage

config_env = os.environ.get('STORAGE_OPTION', 'file')


def storage_option() -> IStorageOption:
    if(config_env == "file"):
        return FileStorage
