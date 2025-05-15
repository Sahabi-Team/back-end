import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from authentication.models import User  # or your custom user model
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs


class CustomCORSHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Add CORS headers to every response
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept, Origin, X-Requested-With"

        return response
# myproject/middleware.py
@database_sync_to_async
def get_user_from_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=payload['user_id'])
        return user
    except Exception:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Extract token from query string
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token')
        if token:
            token = token[0]  # get first token if list
            scope['user'] = await get_user_from_token(token)
        else:
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)
