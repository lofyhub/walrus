import jwt
from fastapi import HTTPException, status
from config import settings
from .schemas import UserSignup
from datetime import datetime, timedelta, timezone

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM


def sign_jwt(user: UserSignup):
    payload = {"user_id": str(user.id), "exp": datetime.utcnow() + timedelta(hours=24)}

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        expiration_time = datetime.fromtimestamp(
            decoded_token.get("exp", 0), timezone.utc
        )

        if expiration_time >= datetime.now(timezone.utc):
            return decoded_token
    except Exception as e:
        return None


#  Utility function to get user from token
def get_user_from_token(token: str):
    user_from_token = decode_jwt(token)
    if user_from_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )
    return user_from_token
