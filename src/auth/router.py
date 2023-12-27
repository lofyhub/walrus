from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from .schemas import SQLAlchemyErrorMessage, SuccessResponse, LoginPayload
from .auth import sign_jwt
from users.models import User
from sqlalchemy.exc import SQLAlchemyError

# Create an API router
router = APIRouter()
# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Endpoint for login
@router.post("/login/", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def login_user(login_payload: LoginPayload, db=Depends(get_db)):
    try:
        check_user = db.query(User).filter(User.email == login_payload.email).first()

        if not check_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Email {login_payload.email} not registered",
            )

        if check_user.name != login_payload.fullname:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Incorrect credentials"
            )

        access_token = sign_jwt(check_user)
        response = SuccessResponse(
            status=str(status.HTTP_200_OK),
            access_token=access_token,
            user=check_user,
            message="Login successfull",
        )
        return response
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SQLAlchemyErrorMessage,
        )


# Export the router
auth_routes = router
