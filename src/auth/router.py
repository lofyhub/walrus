from fastapi import status, HTTPException, APIRouter, Response, Query
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from .schemas import  SQLAlchemyErrorMessage, SuccessResponse, LoginPayload
from .auth import sign_jwt
from users.models import User
from sqlalchemy.exc import SQLAlchemyError

# Create a database session
db = SessionLocal()

# Create an API router
router = APIRouter()

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Endpoint for saving review
@router.get('/login/', response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def login_user(login_payload: LoginPayload):
    try:
        check_user = db.query(User).filter(User.email == login_payload.email).first()

        if check_user is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Email {login_payload.email} not registered")
        
        if check_user.name != login_payload.fullname:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Incorrect credential")
        
        access_token = sign_jwt(check_user)
        response = SuccessResponse(status=status.HTTP_200_OK, access_token=access_token , message="Login successfull")
        return response
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)


# Export the router
auth_routes = router