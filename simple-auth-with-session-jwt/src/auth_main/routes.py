import aiohttp_jinja2

from aiohttp import web, log
from aiohttp_session import new_session, get_session

from . import data_models


routes = web.RouteTableDef()
data_models.create_example_storage()


def protected(handler):
    async def wrapper(request: web.Request, *args, **kwargs):
        app = request.app
        router = app.router

        session = await get_session(request)

        if 'user_id' not in session:
            return web.HTTPFound(router['login'].url_for())

        app['user_id'] = session['user_id'] 
        
        return await handler(request, *args, **kwargs)

    return wrapper


@routes.get('/', name='index')
@protected
@aiohttp_jinja2.template("index.j2")   
async def index(request: web.Request) -> dict:
    app = request.app
    user_id = app.get('user_id', None)
    return {'user_id': user_id}


@routes.get('/login', name='login')
@aiohttp_jinja2.template("login.j2")
async def login_page(request: web.Request) -> dict:
    return {}


@routes.post('/login')
async def login(request: web.Request) -> web.HTTPFound:
    router = request.app.router
    post_data = await request.post()
    user = None
    try:
        user: data_models.User = data_models.UserStorage.get_user(email = post_data.get('email', None))
        user.match_password(post_data.get('password', None))

        session = await new_session(request)
        session['user_id'] = user.id
    
        return web.HTTPFound(router['index'].url_for())

    except (data_models.UserStorage.UserNotFound, data_models.User.PasswordDoesNotMatch) as e:
        log.server_logger.debug(e)
        return web.HTTPFound(router['login'].url_for())        

