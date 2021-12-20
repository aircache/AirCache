class IStorageOption:
    @staticmethod
    def config_has_api(request) -> bool:
        """check if the api exists"""
        pass
    # Create new redis key

    @staticmethod
    def config_load_headers(cache_key, val, exp):
        """Creates the header object from storage"""
        pass
    # Get value of key

    @staticmethod
    def config_is_scoped(cache_key, *path):
        """Retrieves the scope object from storage"""
        pass
