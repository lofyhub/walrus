from fastapi import status, HTTPException, APIRouter, Response, Query, Depends
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from .schemas import  SQLAlchemyErrorMessage, SaveResponse, UserPayload, UserResponse, UserData, SaveUser, GetUser
from .models import User
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from auth.auth_bearer import JWTBearer
from auth.auth import sign_jwt

# Create a database session
db = SessionLocal()

# Create an API router
router = APIRouter()

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Endpoint for saving review

@router.post('/users/', response_model=SaveResponse, status_code=status.HTTP_201_CREATED)
async def save_user(user_payload: UserPayload):
    try:
        check_email = db.query(User).filter(User.email == user_payload.email).first()
        check_tel_number = db.query(User).filter(User.tel_number == user_payload.tel_number).first()

        if check_email is not None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Email {user_payload.email} already registered")
        
        if check_tel_number is not None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Tel number already registered") 
        
        new_user = User(
            name=user_payload.fullname,
            email=user_payload.email,
            picture=user_payload.picture,
            tel_number=user_payload.tel_number,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        access_token = sign_jwt(new_user)

        user_data = UserData(
            id=new_user.id,
            name=new_user.name,
            email=new_user.email,
            tel_number=new_user.tel_number,
            picture=new_user.picture,
            access_token=access_token
        )

        response = SaveResponse(
            status=str(status.HTTP_201_CREATED),
            message="User successfully saved",
            user=user_data,
        )

        return response
    except IntegrityError as e:
        if "UNIQUE constraint failed: users.id" in str(e):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save user: Duplicate ID detected")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save user")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to save user:{e}")



# Endpoint for retrieving users
@router.get('/users/', response_model=GetUser, status_code=status.HTTP_200_OK) 
async def get_users(skip: int = 0, limit: int = 100):
    try:
        # return only none deleted users
        all_users = db.query(User).filter(User.is_deleted == False).offset(skip).limit(limit).all()
        # Convert User objects to UserResponse objects
        user_responses = [
            UserResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                picture=user.picture,
                is_deleted=user.is_deleted,
                tel_number=user.tel_number,
                created_at=user.created_at,
            )
            for user in all_users
        ]
        
        users = GetUser(
            status=str(status.HTTP_200_OK),
            data= user_responses,
            users= len(user_responses), 
        )
        return users
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)


# Endpoint for retrieving a single user
@router.get('/user/',dependencies=[Depends(JWTBearer())], response_model=UserPayload, status_code=status.HTTP_200_OK)
async def get_single_user(user_id: str = Query(...,min_length=10)):
    try:
        single_user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
        
        if single_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
        return single_user
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)



# Endpoint for updating a review
@router.put('/users/{user_id}/', dependencies=[Depends(JWTBearer())],  response_model=SaveResponse, status_code=status.HTTP_200_OK)
async def update_a_user(user_id: int, user_to_update: UserPayload):
    try:
        entry_to_update = db.query(User).filter(User.id == user_id).first()
        print(entry_to_update)

        if entry_to_update is None:
            raise HTTPException(status_code=400, detail=f"User with id {user_id} was not found")
        elif entry_to_update.email != user_to_update.email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Email {user_to_update.email} cannot be different")
        
        entry_to_update.name = user_to_update.fullname
        entry_to_update.email = user_to_update.email
        entry_to_update.picture = user_to_update.picture
        entry_to_update.created_at = datetime.now()

        db.commit()
        response = SaveResponse(status='Ok', message=f"User with id {user_id} updated successfully.")
        return Response(content=response.json(), media_type='application/json', status_code=status.HTTP_200_OK)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)



# Endpoint for deleting a review
@router.delete('/users/{user_id}/', dependencies=[Depends(JWTBearer())],  response_model = SaveResponse, status_code=status.HTTP_200_OK)
async def delete_a_user(user_id: str):
    try:
        user_to_delete = db.query(User).filter(User.id == user_id).first()

        if user_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} was not found")
        
        # soft delete
        user_to_delete.is_deleted = True

        db.commit()
        response = SaveResponse(status='Ok', message=f"User with id {user_id} was successfully deleted")
        return Response(content=response.json(), media_type='application/json', status_code=status.HTTP_200_OK)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)


# Export the router
users_routes = router