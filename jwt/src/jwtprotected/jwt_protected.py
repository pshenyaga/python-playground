import json
import jwt

from aiohttp import web
from datetime import datetime, timedelta

from .models import User

JWT_SECRET = 'jwt_secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 20

User.objects.create('user@example.com', 'hard_password', True)

async def login(request: web.Request) -> web.Response:
    post_data = await request.post()
    email = post_data.get('email', None)
    password = post_data.get('password', None)
    
    if not email or not password:
        # Handle wrong params in post body
        pass
    
    try:
        user: User = User.objects.get(email=email)
        user.match_password(password)

    except (User.DoesNotExists, User.PasswordDoesNotMatch):
        return web.json_response(data={'message': 'Wrong credentials'}, status=400)

    payload = {
        'user_id': user.id,
        'exp':  datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

    return web.json_response({'token': jwt_token})


app = web.Application()
app.router.add_post('/login', login)