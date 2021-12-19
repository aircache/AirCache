class IStorageOption:
    def config_has_api(request) -> bool:
        """check if the api exists"""
        pass
    # Create new redis key
    def config_load_headers(cache_key, val, exp):
        """Creates the header object from storage"""
        pass
    # Get value of key
    def config_is_scoped(cache_key):
        """Retrieves the scope object from storage"""
        pass