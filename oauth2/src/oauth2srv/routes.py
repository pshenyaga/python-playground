import aiohttp_jinja2
import random

from aiohttp import web
from string import ascii_letters
from oauth2helpers import build_url


routes = web.RouteTableDef()

@routes.get('/')
@aiohttp_jinja2.template('index.html.j2')
async def index(request: web.Request) -> dict:
    # return web.Response(text="OAuth2 server")
    return {}

@routes.get('/authorize')
@aiohttp_jinja2.template('authorize.html.j2')
async def authorize(request: web.Request) -> dict:
    clients_db: list = request.app['clients_db']
    requests_db: dict = request.app['requests_db']
    
    response_type = request.query.get('response_type', None)
    client_id = request.query.get('client_id', None)
    redirect_uri = request.query.get('redirect_uri', None)

    if not response_type or not redirect_uri or not client_id:
        # Wrong request. Display error page
        raise web.HTTPBadRequest()

    client = next((c for c in clients_db if c['client_id'] == client_id), None)

    if not client:
        return {'error': 'Unknown client'}

    if redirect_uri not in client['redirect_uris']:
        return {'error': 'Invalid redirect URI'}

    req_id = ''.join(random.choices(ascii_letters, k=8))
    requests_db.update({req_id: request.query})

    return { 'client_id': client['client_id'], 'req_id': req_id }

@routes.post('/approve')
async def approve(request: web.Request) -> web.Response:
    requests_db: dict = request.app['requests_db']
    data = await request.post()

    request_id = data.get('reqid', None)
    origin_request = requests_db.get(request_id, None)

    if not origin_request:
        return web.Response(text='No matching authorization request')

    if 'approve' in data:
        print('access approved')
        return web.Response(text='Access approved')
    else:
        redirect_url = build_url(origin_request['redirect_uri'], {'error': 'access_denied'})
        raise web.HTTPFound(location=redirect_url)

