import json

from aiohttp import web
from multidict import MultiDictProxy, MultiDict

from .utils import deserialize_multidict

class Client:
    """Client for simple oaut2 database
    """
    def __init__(self):
        self.db = {
            'codes': {},
            'requests': {},
            'clients': [
                {
                    'client_id': 'oauth-client-1',
                    'client_secret': 'oauth-client-secret-1',
                    'redirect_uris': ['http://localhost:9000/callback']
                }]
        }

    async def add_code(self, _code: str, query: MultiDictProxy) -> None:
        """Store request identified by code in database

        Args:
            _code (str): Response code.
            query (MultiDictProxy): query to store
        """
        # TODO: check if code already exists in database
        self.db['codes'].update({_code: json.dumps({key: query.getall(key) for key in query.keys()})})

    async def delete_code(self, _code: str) -> MultiDictProxy:
        """Deletes stored request from codes.

        Args:
            _code (str): Code

        Returns:
            MultiDictProxy: Removed request
        """
        # TODO: raise error if request doesn't exist
        return deserialize_multidict(self.db['codes'].get(_code, None))

    async def get_code(self, _code: str) -> MultiDictProxy:
        return deserialize_multidict(self.db['codes'].get(_code, None))

    async def add_request(self, _id: str, query: MultiDictProxy) -> None:
        """Store request in database

        Args:
            _id (str): request id
            query (MultiDictProxy): query to store
        """
        # TODO: check if _id already exists in database
        self.db['requests'].update({_id: json.dumps({key: query.getall(key) for key in query.keys()})})

    async def delete_request(self, _id: str) -> MultiDictProxy:
        """Deletes stored request from database and returns it

        Args:
            _id (str): request id
        Returns:
            request (MultiDictProxy): 
        """

        #TODO: raise error if request doesn't exist
        return deserialize_multidict(self.db['requests'].pop(_id, None))

    async def get_request(self, _id: str) -> MultiDictProxy:
        return deserialize_multidict(self.db['requests'].get(_id, None))

    async def get_client_by_id(self, _id: str) -> dict:
        return next((client for client in self.db['clients'] if client['client_id'] == _id), None)


def init(app: web.Application) -> None:
    client = Client()
    app['data_handler'] = client

if __name__ == "__main__":
    pass