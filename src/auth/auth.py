import jwt
from config.config import settings
from schema.schema import UserPayload
from datetime import datetime, timedelta

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM

def sign_jwt(user: UserPayload):
    expiration_time = datetime.utcnow() + timedelta(hours=24)
    payload = {
        "user_id": user.fullname,
        "exp": expiration_time
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token.get('exp', 0) >= datetime.utcnow() else {}
    except jwt.InvalidTokenError:
        return {}

def token_response(token: str):
    return {
        "access_token": token
    }