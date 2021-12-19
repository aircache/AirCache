class ICacheOption:
    def key_params(request) -> str:
        """Returns the cache key"""
        pass
    # Create new redis key
    def create_key(cache_key, val, exp) -> None:
        """Creates the cache object"""
        pass
    # Get value of key
    def get_key(cache_key):
        """Retrieves the cache object"""
        pass
    # Check key exist
    def exist_key(cache_key) -> bool:
        """Checks if the key exists"""
        pass
