import aiohttp_jinja2
import jinja2

from aiohttp import web

from .routes import routes

client = {
    'client_id': 'oauth-client-1',
    'client_secret': 'oauth-client-secret-1',
    'redirect_uris': ['http://localhost:9000/callback']
}

auth_server = {
    'authorization_endpoint': 'http://localhost:9001/authorize',
    'token_endpoint': 'http://localhost:9001/token'
}

protected_resource = 'http://localhost:9002/resource'
wordApi = 'http://localhost:9002/words'
produceApi = 'http://localhost:9002/produce'
favoritesApi = 'http://localhost:9002/favorites'

def init_app(_client: dict, _auth_server: dict) -> web.Application: 
    _app = web.Application()

    # jinja2 template renderer
    aiohttp_jinja2.setup(_app, loader=jinja2.PackageLoader('oauth2client', 'templates'))

    _app.add_routes(routes)
    _app['config'] = {
        'client': _client,
        'auth_server': _auth_server, 'protected_resource': protected_resource}

    return _app


def main():
    app = init_app(client, auth_server)
    web.run_app(app, host='127.0.0.1', port=9000)