from fastapi import status, APIRouter, Depends, Header
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from database import get_db
from .schemas import (
    SaveResponse,
    UserPayload,
    UserResponse,
    UserData,
    UserInfo,
)
from datetime import datetime
from auth.auth_bearer import JWTBearer
from auth.auth import sign_jwt
from .services import (
    save_user_to_db,
    query_user_by_email,
    query_user_by_number,
    query_users,
    query_user,
)
from .exceptions import exception_handler
from auth.auth import get_user_from_token


# Create an API router
router = APIRouter()

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Endpoint for saving a user
@router.post("/users/")
async def save_user(user_payload: UserPayload, db=Depends(get_db)):
    try:
        check_email = query_user_by_email(db, user_payload)
        check_tel_number = query_user_by_number(db, user_payload)

        if check_email:
            message = f"Email `{user_payload.email}` already registered"
            return JSONResponse(
                content={"status": "403", "message": message},
                status_code=status.HTTP_403_FORBIDDEN,
            )

        if check_tel_number:
            message = f"Telephone number `{user_payload.tel_number}` already registered"
            return JSONResponse(
                content={"status": "403", "message": message},
                status_code=status.HTTP_403_FORBIDDEN,
            )

        new_user = save_user_to_db(db, user_payload)
        access_token = sign_jwt(new_user)

        user_data = UserData(
            id=new_user.id,
            name=new_user.name,
            email=new_user.email,
            picture=new_user.picture,
            access_token=access_token,
        )

        response = SaveResponse(
            status=str(status.HTTP_201_CREATED),
            message="User successfully saved",
            user=user_data,
        )

        return JSONResponse(
            content=response.dict(), status_code=status.HTTP_201_CREATED
        )
    except Exception as error:
        exception_handler(error)


# Endpoint for retrieving users
@router.get(
    "/users/",
)
async def get_users(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    try:
        all_users = await query_users(db, skip, limit)

        # Map User objects to UserResponse objects
        user_responses = [
            UserResponse(
                id=user.id,
                name=user.name,
                picture=user.picture,
                tel_number=user.tel_number,
                created_at=user.created_at,
            )
            for user in all_users
        ]

        response_data = {
            "status": str(status.HTTP_200_OK),
            "data": jsonable_encoder(user_responses),
            "users": len(user_responses),
        }

        return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)
    except Exception as error:
        exception_handler(error)


@router.get(
    "/user/{user_id}",
    dependencies=[Depends(JWTBearer())],
)
async def get_single_user(user_id: str, db=Depends(get_db)):
    try:
        single_user = await query_user(db, user_id)

        if single_user is None:
            response_data = {
                "status": "404",
                "message": f"User with id `{user_id}` not found",
            }
            return JSONResponse(
                content=response_data, status_code=status.HTTP_404_NOT_FOUND
            )

        user_info = UserInfo(
            id=single_user.id,
            fullname=single_user.name,
            email=single_user.email,
            tel_number=single_user.tel_number,
            picture=single_user.picture,
            created_at=single_user.created_at,
        )

        response_data = {
            "status": "200",
            "user": jsonable_encoder(user_info),
            "message": "Successful",
        }

        return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)

    except Exception as error:
        exception_handler(error)


# Endpoint for updating a review
@router.put(
    "/users/{user_id}/",
    dependencies=[Depends(JWTBearer())],
    response_model=SaveResponse,
    status_code=status.HTTP_200_OK,
)
async def update_a_user(
    user_id: str,
    user_to_update: UserPayload,
    db=Depends(get_db),
    authorization: str = Header(None),
):
    try:
        token = (
            authorization.split(" ")[1]
            if authorization and " " in authorization
            else None
        )

        entry_to_update = await query_user(db, user_id)
        user_info_from_token = get_user_from_token(token)

        if not entry_to_update:
            response_data = {
                "status": "404",
                "message": f"User with id `{user_id}` was not found",
            }
            return JSONResponse(
                content=response_data, status_code=status.HTTP_404_NOT_FOUND
            )

        if user_info_from_token["user_id"] != entry_to_update.id:
            response_data = {
                "status": "403",
                "message": "You can only update your own resource",
            }
            return JSONResponse(
                content=response_data, status_code=status.HTTP_403_FORBIDDEN
            )

        if entry_to_update.email != user_to_update.email:
            response_data = {
                "status": "403",
                "message": f"Email `{user_to_update.email}` cannot be updated",
            }
            return JSONResponse(
                content=response_data, status_code=status.HTTP_403_FORBIDDEN
            )

        entry_to_update.name = user_to_update.fullname
        entry_to_update.email = user_to_update.email
        entry_to_update.picture = user_to_update.picture
        entry_to_update.created_at = datetime.now()

        db.commit()

        response_data = {
            "status": "Ok",
            "message": f"User with id `{user_id}` updated successfully.",
        }
        return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)

    except Exception as error:
        exception_handler(error)


# Endpoint for deleting a review
@router.delete(
    "/users/{user_id}/",
    dependencies=[Depends(JWTBearer())],
    response_model=SaveResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_a_user(
    user_id: str, db=Depends(get_db), authorization: str = Header(None)
):
    try:
        token = (
            authorization.split(" ")[1]
            if authorization and " " in authorization
            else None
        )
        user_to_delete = await query_user(db, user_id)

        if not user_to_delete:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "status": "404",
                    "message": f"User with id `{user_id}` was not found",
                },
            )

        user_info_from_token = get_user_from_token(token)

        if user_info_from_token["user_id"] != user_to_delete.id:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "status": "403",
                    "message": "You can only delete your resource",
                },
            )

        # Soft delete
        user_to_delete.is_deleted = True
        db.commit()

        response = SaveResponse(
            status="200", message=f"User with id {user_id} was successfully deleted"
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=response.model_dump_dict()
        )

    except Exception as error:
        exception_handler(error)


# Export the router
users_routes = router
