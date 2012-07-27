
# If no root URL is found, we raise this...
class NoRootURL(Exception):
    pass

# If there is more than one...
class MultipleRootURLs(Exception):
    pass

class IllegalFileExtension(Exception):
    """File extension on upload is not allowed"""
    pass
