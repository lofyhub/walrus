from fastapi import status, HTTPException, APIRouter, Response, Form, UploadFile, Depends
from typing import Annotated, List, Union
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from .schemas import ResponseBusiness, SaveResponse, GetBusinesses, BusinessNotFound
from .models import Business
from datetime import datetime
from utils import upload_image
from auth.auth_bearer import JWTBearer
from .error_handler import exception_handler
import uuid

# Create a database session
db = SessionLocal()

# Create an API router
router = APIRouter()

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Endpoint for saving businesse
@router.post('/businesses/',dependencies=[Depends(JWTBearer())],  response_model=SaveResponse, status_code=status.HTTP_201_CREATED)
async def save_business(
    images: List[UploadFile],
    name: Annotated[str, Form()],
    handle: Annotated[str, Form()],
    location: Annotated[str, Form()],
    county: Annotated[str, Form()],
    town: Annotated[str, Form()],
    opening: Annotated[str, Form()],
    closing: Annotated[str, Form()],
    business_description: Annotated[str, Form()],
    telephone_number: Annotated[str, Form()],
    category: Annotated[str, Form()],
    user_id: Annotated[str, Form()],
    amenities: Annotated[List[str], Form()]
    ):
    try:
        uploaded_image_paths = await upload_image(images)

        new_business = Business(
                name =  name,
                handle = handle,
                images = uploaded_image_paths,
                location = location,
                county = county,
                town = town,
                opening_hours = [opening, closing],
                business_description = business_description,
                telephone_number = telephone_number,
                category = category,
                user_id = uuid.UUID(user_id),
                amenities = amenities,
                verified = False,
                created_at = datetime.now(),
        )

        db.add(new_business)
        db.commit()
        response = SaveResponse(status="201", message="Business successfully saved")
        return Response(content=response.model_dump_json(), media_type='application/json', status_code=status.HTTP_201_CREATED)
    except Exception as e:
        exception_handler(e)

# Endpoint for retrieving  business
@router.get('/businesses/', response_model=Union[GetBusinesses, BusinessNotFound], status_code=status.HTTP_200_OK)
async def get_businesses(skip: int = 0, limit: int = 100):
    try:
        # return none deleted businesses
        all_businesses: List[ResponseBusiness] = db.query(Business).filter(Business.is_deleted == False).offset(skip).limit(limit).all()

        if all_businesses is None:
            return BusinessNotFound
        
        return GetBusinesses(
            status='200',
            data=all_businesses,
            businesses=str(len(all_businesses))
        )
    except Exception as e:
        exception_handler(e)

# Endpoint for retrieving a single business
@router.get('/businesses/{business_id}/', response_model=Union[ResponseBusiness, BusinessNotFound], response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def get_single_business(business_id: str):
    try:

        business_uuid = uuid.UUID(business_id)
        # return a single business
        single_business: ResponseBusiness = db.query(Business).filter(Business.id == business_uuid and Business.is_deleted == False).first()

        if single_business is None:
            not_found = BusinessNotFound(
                status= str(status.HTTP_404_NOT_FOUND),
                message=f"Business with id {business_id} not found",
            )
            return Response(status_code=status.HTTP_404_NOT_FOUND, content=not_found.model_dump_json(), media_type='application/json') 
        
        return single_business
    except Exception as e:
        exception_handler(e)


# Endpoint for updating a business
@router.put('/businesses/{business_id}/',dependencies=[Depends(JWTBearer())], response_model=Union[SaveResponse, BusinessNotFound], status_code=status.HTTP_200_OK)
async def update_a_business(business_id: int, business_to_update: ResponseBusiness):
    try:
        entry_to_update = db.query(Business).filter(Business.id == business_id and Business.is_deleted == False).first()

        if entry_to_update is None:
            business_not_found = BusinessNotFound(
                message=f"Busineess entry with id {business_id} not found"
                )
            return Response(status_code=status.HTTP_404_NOT_FOUND, content=business_not_found.model_dump_json(), media_type='application/json') 
        
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
        entry_to_update.created_at = datetime.now(),

        db.commit()
        response = SaveResponse(status=status.HTTP_200_OK, message=f"Business with id {business_id} updated successfully.")
        return Response(content=response.json(), media_type='application/json', status_code=status.HTTP_200_OK)
    except Exception as e:
        exception_handler(e)


# Endpoint for deleting a business
@router.delete('/businesses/{business_id}/', dependencies=[Depends(JWTBearer())],  response_model=SaveResponse, status_code=status.HTTP_200_OK)
async def delete_a_business(business_id: int):
    try:
        business_to_delete = db.query(Business).filter(Business.id == business_id and Business.is_deleted == False).first()

        if business_to_delete is None:
            not_found = BusinessNotFound(
                message = f"Business with id {business_id} was not found",
            )
            return Response(content=not_found.model_dump_json(), media_type='application/json', status_code=status.HTTP_404_NOT_FOUND)
        
        # soft delete
        business_to_delete.is_deleted = True

        db.commit()
        response = SaveResponse(status=status.HTTP_200_OK, message=f"Business with id {business_id} was successfully deleted")
        return Response(content=response.json(), media_type='application/json', status_code=status.HTTP_200_OK)
    except Exception as e:
        exception_handler(e)

# Export the router
business_routes = router