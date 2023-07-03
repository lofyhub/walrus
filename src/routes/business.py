from fastapi import status, HTTPException, APIRouter, Response, Form, UploadFile, File
from typing import Annotated, Dict, Any
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal
from schema.schema import ResponseBusiness, BusinessSaveResponse, SQLAlchemyErrorMessage, OkResponse
from models.models import Business
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from auth.auth import decode_jwt
from utils.helpers import upload_image
import json

# Create a database session
db = SessionLocal()

# Create an API router
router = APIRouter()

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# Utility function to get user from token
async def get_user_from_token(token: str):
    user_from_token = decode_jwt(token)
    if not user_from_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return user_from_token


# Endpoint for saving businesse
@router.post('/businesses/', response_model=BusinessSaveResponse, status_code=status.HTTP_201_CREATED)
async def save_business(
    images: List[UploadFile],
    name: Annotated[str, Form()],
    handle: Annotated[str, Form()],
    location: Annotated[str, Form()],
    opening: Annotated[str, Form()],
    closing: Annotated[str, Form()],
    business_description: Annotated[str, Form()],
    telephone_number: Annotated[str, Form()],
    category: Annotated[str, Form()],
    user_id: Annotated[int, Form()],
    amenities: Annotated[List[str], Form()]
    ):
    try:
        print(datetime.now())
        uploaded_image_paths = await upload_image(images)
        print(datetime.now())

        new_business = Business(
                name =  name,
                handle = handle,
                images = uploaded_image_paths,
                location = location,
                opening_hours = [opening, closing],
                business_description = business_description,
                telephone_number = telephone_number,
                category = category,
                user_id = user_id,
                amenities = amenities,
                verified = False,
                creation_date = datetime.now().strftime("%Y-%m-%d"),
        )

        db.add(new_business)
        db.commit()
        response = BusinessSaveResponse(status='Ok', message=f"Business successfully saved")
        return Response(content=response.json(), media_type='application/json', status_code=status.HTTP_201_CREATED)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)



# Endpoint for retrieving  business
@router.get('/businesses/', response_model=List[ResponseBusiness], status_code=status.HTTP_200_OK)
async def get_businesses(skip: int = 0, limit: int = 100):
    try:
        all_businesses: List[ResponseBusiness] = db.query(Business).offset(skip).limit(limit).all()
        print(all_businesses)
        return all_businesses
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)



# Endpoint for updating a business
@router.put('/businesses/{business_id}/',response_model=BusinessSaveResponse, status_code=status.HTTP_200_OK)
async def update_a_business(business_id: int, business_to_update: ResponseBusiness):
    try:
        entry_to_update = db.query(Business).filter(Business.id == business_id).first()

        if entry_to_update is None:
            raise HTTPException(status_code=400, detail=f"Entry with id {business_id} was not found")
        
        uploaded_image_paths = []
        for base64_image in business_to_update.images:
            image_path = await upload_image(base64_image)
            uploaded_image_paths.append(image_path)

        entry_to_update.name = business_to_update.name,
        entry_to_update.handle = business_to_update.handle,
        entry_to_update.images = uploaded_image_paths,
        entry_to_update.location = business_to_update.location,
        entry_to_update.opening = business_to_update.opening,
        entry_to_update.business_description = business_to_update.business_description,
        entry_to_update.telephone_number = business_to_update.telephone_number,
        entry_to_update.category = business_to_update.category,
        entry_to_update.user_id = business_to_update.user_id,
        entry_to_update.creation_date = datetime.now().strftime("%Y-%m-%d"),

        db.commit()
        response = BusinessSaveResponse(status='Ok', message=f"Business with id {business_id} updated successfully.")
        return Response(content=response.json(), media_type='application/json', status_code=status.HTTP_200_OK)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)



# Endpoint for deleting a business
@router.delete('/businesses/{business_id}/', response_model=BusinessSaveResponse, status_code=status.HTTP_200_OK)
async def delete_a_business(business_id: int):
    try:
        business_to_delete = db.query(Business).filter(Business.id == business_id).first()

        if business_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Business with id {business_id} was not found")
        
        db.delete(business_to_delete)
        db.commit()
        response = BusinessSaveResponse(status='Ok', message=f"Business with id {business_id} was successfully deleted")
        return Response(content=response.json(), media_type='application/json', status_code=status.HTTP_200_OK)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)

# Export the router
business_routes = router