import aiohttp_jinja2
import json

from aiohttp import web, ClientSession
from oauth2helpers import build_url, encode_client_credential

routes = web.RouteTableDef()

@routes.get('/')
@aiohttp_jinja2.template('index.html.j2')
async def index(request: web.Request) -> web.Response:
    client: dict = request.app['config']['client']
    return {'access_token': client.get('access_token', None)}

@routes.get('/authorize')
async def authorize(request: web.Request) -> web.Response:
    # TODO: add cross site protection
    app = request.app
    client_config = app['config']['client']
    auth_server_config = app['config']['auth_server']
    authorize_url = build_url(
        auth_server_config['authorization_endpoint'],
        {
            'response_type': 'code',
            'client_id': client_config['client_id'],
            'redirect_uri': client_config['redirect_uris'][0]
        })

    raise web.HTTPFound(location=authorize_url)

@routes.get('/callback')
async def callback(request: web.Request):
    session: ClientSession = None
    client_config: dict = request.app['config']['client']
    auth_server_config = request.app['config']['auth_server']

    # TODO: check for errors in query
    auth_code: str = request.query.get('code', None)
    form_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': client_config['redirect_uris'][0]
    }

    headers = {
        'Authorization': 'Basic ' + encode_client_credential(client_config['client_id'], client_config['client_secret'])
    }

    async with ClientSession() as session:
        async with session.post(auth_server_config['token_endpoint'], headers=headers, json=form_data) as response:
            # TODO: Check for errors
            json_res: dict = await response.json()
            client_config.update({'access_token': json_res.get('access_token', None)})
            raise web.HTTPFound(location='/')

    return web.Response(text='code: {}'.format(auth_code))
