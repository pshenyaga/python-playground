import urllib.parse as urllib
import json
from multidict import MultiDict, MultiDictProxy

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


def deserialize_multidict(json_string: str) -> MultiDictProxy:
    if json_string:
        result = MultiDict()
        parsed: dict = json.loads(json_string)
        for key in parsed.keys():
            for item in parsed[key]:
                result.add(key, item)

        return MultiDictProxy(result)
    return None