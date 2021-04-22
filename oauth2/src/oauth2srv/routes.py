import aiohttp_jinja2
import random
import json

from aiohttp import web
from string import ascii_letters
from webargs.aiohttpparser import parser

from oauth2helpers import build_url, decode_client_credential
from oauth2helpers.data_handler import Client as DataHandlerClient

from .models.request_schemas import (
    authorize_schema,
    approve_schema,
    token_schema_headers,
    token_schema_json
)


routes = web.RouteTableDef()

@parser.error_handler
def he(err, *args, **kwargs):
# def he(err, req, schema, *, error_status_code, error_header):
    raise err

@routes.get('/')
@aiohttp_jinja2.template('index.html.j2')
async def index(request: web.Request) -> dict:
    # return web.Response(text="OAuth2 server")
    return {}


@routes.get('/authorize')
@aiohttp_jinja2.template('authorize.html.j2')
async def authorize(request: web.Request) -> dict:
    dh: DataHandlerClient = request.app['data_handler']
    args = await parser.parse(**authorize_schema, req=request)

    client = await dh.get_client_by_id(args['client_id'])

    if not client:
        return {'error': 'Unknown client'}

    if args['redirect_uri'] not in client['redirect_uris']:
        return {'error': 'Invalid redirect URI'}

    req_id = ''.join(random.choices(ascii_letters, k=8))
    await dh.add_request(req_id, request.query)

    return {'client_id': client['client_id'], 'req_id': req_id}


@routes.post('/approve')
@aiohttp_jinja2.template('base.html.j2')
async def approve(request: web.Request) -> dict:
    dh: DataHandlerClient = request.app['data_handler']
    args = await parser.parse(**approve_schema, req=request)

    origin_request = await dh.delete_request(args['reqid'])

    if not origin_request:
        return {'title': 'OAuth server', 'error': 'No matching athorization request'}

    if 'Approve' == args['approve']:
        if origin_request['response_type'] == 'code':
            code = ''.join(random.choices(ascii_letters, k=16))

            await dh.add_code(code, origin_request)

            redirect_url_params = {'code': code}

            if 'state' in origin_request:
                redirect_url_params['state'] = origin_request['state']

            redirect_url = build_url(origin_request['redirect_uri'], redirect_url_params)

        else:
            redirect_url = build_url(origin_request['redirect_uri'], {'error', 'usupported_response_type'})

    else:
        redirect_url = build_url(origin_request['redirect_uri'], {'error': 'access_denied'})

    raise web.HTTPFound(location=redirect_url)


@routes.post('/token')
async def token(request: web.Request) -> web.Response:
    dh: DataHandlerClient = request.app['data_handler']
    args_headers = await parser.parse(**token_schema_headers, req=request)
    args_json = await parser.parse(**token_schema_json, req=request)

    if 'authorization' in args_headers:
        client_id, client_secret = decode_client_credential(
            args_headers['authorization'].split()[1])

    if 'client_id' in args_json:
        if client_id:
            err_body = json.dumps({'error': 'invalid_client'})
            return web.HTTPUnauthorized(content_type='application/json', text=err_body)

        client_id = args_json['client_id']
        client_secret = args_json.get('client_secret', '')

    client = await dh.get_client_by_id(client_id)

    if not client or client['client_secret'] != client_secret:
        err_body = json.dumps({'error': 'invalid_client'})
        raise web.HTTPUnauthorized(content_type='application/json', text=err_body)

    if args_json['grant_type'] == 'authorization_code' and 'code' in args_json:
        origin_request = await dh.delete_code(args_json['code'])

        if origin_request and origin_request['client_id'] == client_id:
            access_token = ''.join(random.choices(ascii_letters, k=16))
            # TODO: save access_token for later use
            return web.json_response({'access_token': access_token, 'token_type': 'Bearer'})

        else:
            err_text = json.dumps({'error': 'invalid_grant'})
            raise web.HTTPBadRequest(content_type='application/json', text=err_text)

    else:
        err_text = json.dumps({'error': 'unsupported_grant_type'})
        raise web.HTTPBadRequest(content_type='application/json', text=err_text)
