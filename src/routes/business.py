from fastapi import status, HTTPException, APIRouter, Response
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal
from schema.schema import BusinessPayload, get_county_str,ResponseBusiness, BusinessSaveResponse, SQLAlchemyErrorMessage
from models.models import Business
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from auth.auth import decode_jwt
from utils.helpers import upload_image

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
async def save_business(business: BusinessPayload):
    try:
        uploaded_image_paths = await upload_image(business.images)

        new_business = Business(
                name = business.name,
                handle=business.handle,
                images=uploaded_image_paths,
                location=get_county_str(business.location),
                opening=business.opening,
                business_description=business.business_description,
                telephone_number=business.telephone_number,
                category=business.category,
                user_id=business.user_id,
                amenities=business.amenities,
                verified = False,
                creation_date=datetime.now().strftime("%Y-%m-%d"),
        )

        db.add(new_business)
        db.commit()
        response = BusinessSaveResponse(status='Ok', message=f"{business.name} was successfully saved to the database")
        return Response(content=response.json(), media_type='application/json', status_code=status.HTTP_201_CREATED)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)



# Endpoint for retrieving  business
@router.get('/businesses/',status_code=status.HTTP_200_OK)
async def get_businesses():
    try:
        all_businesses = db.query(Business).all()
        return all_businesses
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)



# Endpoint for updating a business
@router.put('/businesses/{business_id}/',response_model=BusinessSaveResponse, status_code=status.HTTP_200_OK)
async def update_a_business(business_id: int, business_to_update: ResponseBusiness):
    try:
        entry_to_update = db.query(Business).filter(Business.id == business_id).first()

        if entry_to_update is None:
            raise HTTPException(status_code=400, detail=f"Entry with the id {business_id} was not found")
        
        uploaded_image_paths = []
        for base64_image in business_to_update.images:
            image_path = await upload_image(base64_image)
            uploaded_image_paths.append(image_path)

        entry_to_update.name = business_to_update.name,
        entry_to_update.handle = business_to_update.handle,
        entry_to_update.images = uploaded_image_paths,
        entry_to_update.location =business_to_update.location,
        entry_to_update.opening=business_to_update.opening,
        entry_to_update.business_description=business_to_update.business_description,
        entry_to_update.telephone_number=business_to_update.telephone_number,
        entry_to_update.category=business_to_update.category,
        entry_to_update.user_id=business_to_update.user_id,
        entry_to_update.creation_date=datetime.now().strftime("%Y-%m-%d"),

        db.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail={"status": "Ok", "message":f"Business with the id {business_id} was updated"})
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)



# Endpoint for deleting a business
@router.delete('/businesses/{business_id}/', response_model=BusinessSaveResponse, status_code=status.HTTP_200_OK)
async def delete_a_business(business_id: int):
    try:
        business_to_delete = db.query(Business).filter(Business.id == business_id).first()

        if business_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Business with the id {business_id} was not found")
        
        db.delete(business_to_delete)
        db.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail={"status" : "Ok", "message" : f"Business with the id {business_id}was successfully deleted"})

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)

# Export the router
business_routes = router