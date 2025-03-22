import jwt
import datetime
from django.conf import settings

def generate_jwt_token(user):
    payload = {
        'id': user.id,
        'email': user.email,
        'user_type': user.user_type,
        'exp': datetime.datetime.utcnow() + settings.JWT_EXPIRATION_DELTA,
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
