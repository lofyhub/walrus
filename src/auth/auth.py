import jwt
from fastapi import HTTPException, status
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
        return decoded_token if decoded_token.get('exp', 0) >= datetime.utcnow() else None
    except jwt.InvalidTokenError:
        return None

def token_response(token: str):
    return {
        "access_token": token
    }


#  Utility function to get user from token
async def get_user_from_token(token: str):
    user_from_token = await decode_jwt(token)
    if user_from_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return user_from_token

