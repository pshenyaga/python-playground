import json

from multidict import MultiDictProxy, MultiDict

from .oauth2helpers import deserialize_multidict

class client:
    """Client for simple oaut2 database
    """
    def __init__(self):
        self.db = {
            'requests': {}
        }

    async def add_request(self, _id: str, query: MultiDictProxy) -> None:
        self.db.update({_id, json.dumps({key: query(key) for key in query.keys()})})

    async def delete_request(self, _id: str) -> MultiDictProxy:
        return deserialize_multidict(self.db.pop(_id, None))

    async def get_request(self, _id: str) -> MultiDictProxy:
        return deserialize_multidict(self.db.get(_id, None))


if __name__ == "__main__":
    pass