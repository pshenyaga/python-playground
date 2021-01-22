import urllib.parse as urllib

def build_url (base: str, options: dict, fragment: str = '') -> str:
    """Generates URL

    Args:
        base (str): Base URL with protocol and path. For example 'http://example.com/first-example'
        options (dict): Dict which will be converted to query string
        fragment (str, optional): Fragment identifier. Defaults to ''.

    Returns:
        str: Generated URL
    """

    url_fragments = list(urllib.urlparse(base))
    url_fragments[4] = urllib.urlencode(options)
    url_fragments[5] = urllib.quote(fragment)
    
    return urllib.urlunparse(url_fragments)