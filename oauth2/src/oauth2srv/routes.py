import aiohttp_jinja2
import random
import json

from aiohttp import web
from string import ascii_letters
from oauth2helpers import build_url, decode_client_credential
from oauth2helpers.data_handler import Client as DataHandlerClient


routes = web.RouteTableDef()

@routes.get('/')
@aiohttp_jinja2.template('index.html.j2')
async def index(request: web.Request) -> dict:
    # return web.Response(text="OAuth2 server")
    return {}

@routes.get('/authorize')
@aiohttp_jinja2.template('authorize.html.j2')
async def authorize(request: web.Request) -> dict:
    dh: DataHandlerClient = request.app['data_handler']

    response_type = request.query.get('response_type', None)
    client_id = request.query.get('client_id', None)
    redirect_uri = request.query.get('redirect_uri', None)

    if not response_type or not redirect_uri or not client_id:
        # Wrong request. Display error page
        raise web.HTTPBadRequest()

    client = await dh.get_client_by_id(client_id)

    if not client:
        return {'error': 'Unknown client'}

    if redirect_uri not in client['redirect_uris']:
        return {'error': 'Invalid redirect URI'}

    req_id = ''.join(random.choices(ascii_letters, k=8))
    await dh.add_request(req_id, request.query)

    return {'client_id': client['client_id'], 'req_id': req_id}

@routes.post('/approve')
@aiohttp_jinja2.template('base.html.j2')
async def approve(request: web.Request) -> dict:
    dh: DataHandlerClient = request.app['data_handler']

    data = await request.post()

    request_id = data.get('reqid', None)
    origin_request = await dh.delete_request(request_id)

    if not origin_request:
        return {'title': 'OAuth server', 'error': 'No matching athorization request'}

    if 'approve' in data:
        if origin_request['response_type'] == 'code':
            code = ''.join(random.choices(ascii_letters, k=16))

            await dh.add_code(code, origin_request)

            redirect_url = build_url(origin_request['redirect_uri'], {'code': code})
        else:
            redirect_url = build_url(origin_request['redirect_uri'], {'error', 'usupported_response_type'})
    else:
        redirect_url = build_url(origin_request['redirect_uri'], {'error': 'access_denied'})

    raise web.HTTPFound(location=redirect_url)

@routes.post('/token')
async def token(request: web.Request) -> web.Response:
    dh: DataHandlerClient = request.app['data_handler']

    data = await request.json()

    auth = request.headers.get('authorization', None)
    if auth:
        client_id, client_secret = decode_client_credential(auth.split()[1])

    if 'client_id' in data:
        if client_id:
            err_body = json.dumps({'error': 'invalid_client'})
            raise web.HTTPUnauthorized(content_type='application/json', text=err_body)

        client_id = data.get('client_id', None)
        client_secret = data.get('client_secret')

    client = await dh.get_client_by_id(client_id)

    if not client or client['client_secret'] != client_secret:
        err_body = json.dumps({'error': 'invalid_client'})
        raise web.HTTPUnauthorized(content_type='application/json', text=err_body)

    grant_type = data.get('grant_type')
    if grant_type == 'authorization_code':
        origin_request = await dh.delete_code(data.get('code', None))
        if origin_request and origin_request.get('client_id', None) == client_id:
            access_token = ''.join(random.choices(ascii_letters, k=16))
            # TODO: save access_token for later use
            return web.json_response({'access_token': access_token, 'token_type': 'Bearer'})
        else:
            err_text = json.dumps({'error': 'invalid_grant'})
            raise web.HTTPUnauthorized(content_type='application/json', text=err_text)
    else:
        err_text = json.dumps({'error': 'unsupported_gran_type'})
        raise web.HTTPUnauthorized(content_type='application/json', text=err_text)
