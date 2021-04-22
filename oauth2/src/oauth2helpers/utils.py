import urllib.parse as urlparse
import json

from base64 import b64encode, b64decode
from multidict import MultiDict, MultiDictProxy

def encode_client_credential(client_id: str, client_secret: str) -> str:
    return b64encode(urlparse.quote("{}:{}".format(client_id, client_secret)).encode('ascii')).decode()


def decode_client_credential(encoded: str) -> (str, str):
    return tuple(urlparse.unquote(b64decode(encoded).decode()).split(':'))


def build_url (base: str, options: dict, fragment: str = '') -> str:
    """Generates URL

    Args:
        base (str): Base URL with protocol and path. For example 'http://example.com/first-example'
        options (dict): Dict which will be converted to query string
        fragment (str, optional): Fragment identifier. Defaults to ''.

    Returns:
        str: Generated URL
    """

    url_fragments = list(urlparse.urlparse(base))
    url_fragments[4] = urlparse.urlencode(options)
    url_fragments[5] = urlparse.quote(fragment)
    
    return urlparse.urlunparse(url_fragments)


def json_to_multidict(json_string: str) -> MultiDictProxy:
    if json_string:
        result = MultiDict()
        parsed: dict = json.loads(json_string)
        for key in parsed.keys():
            for item in parsed[key]:
                result.add(key, item)

        return MultiDictProxy(result)
    return None


if __name__ == "__main__":
    pass
    # encoded = encode_client_credential('oauth-client-1', 'oauth-client-secret-1') 
    # print(encode_client_credential('oauth-client-1', 'oauth-client-secret-1'))
    # print(decode_client_credential(encoded))
