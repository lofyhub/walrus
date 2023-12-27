from fastapi import status, APIRouter, Response, Form, UploadFile, Depends, Header
from typing import Annotated, List, Union
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from database import get_db
from .schemas import (
    ResponseBusiness,
    SaveResponse,
    BusinessNotFound,
    GetBusinesses,
    DeleteResource,
)
from .models import Business
from datetime import datetime
from utils import upload_image
from auth.auth_bearer import JWTBearer
from auth.auth import get_user_from_token
from .error_handler import exception_handler
from .services import save_business_db, query_businesses, query_single_business
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
import uuid
import json

# Create an API router
router = APIRouter()

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Endpoint for saving businesse
@router.post(
    "/businesses/",
    dependencies=[Depends(JWTBearer())],
)
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
    amenities: Annotated[List[str], Form()],
    db: Session = Depends(get_db),
):
    try:
        uploaded_image_paths = await upload_image(images)

        new_business = Business(
            name=name,
            handle=handle,
            images=uploaded_image_paths,
            location=location,
            county=county,
            town=town,
            opening_hours=[opening, closing],
            business_description=business_description,
            telephone_number=telephone_number,
            category=category,
            user_id=uuid.UUID(user_id),
            amenities=amenities,
            verified=False,
        )

        await save_business_db(db, new_business)

        response_data = {
            "status": "201",
            "message": "Business created successfully",
        }

        return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)
    except Exception as error:
        exception_handler(error)


# Endpoint for retrieving  business
@router.get("/businesses/")
async def get_businesses(db: Session = Depends(get_db)):
    try:
        all_businesses = await query_businesses(db)

        if not all_businesses:
            response_message = {
                "status": "200",
                "data": [],
                "businesses": "0",
            }
            return Response(
                content=response_message,
                status_code=status.HTTP_200_OK,
                media_type="application/json",
            )
        response_data = GetBusinesses(
            status="200",
            data=all_businesses,
            businesses=str(len(all_businesses)),
        )
        return Response(
            content=response_data.model_dump_json(),
            status_code=status.HTTP_200_OK,
            media_type="application/json",
        )
    except Exception as error:
        exception_handler(error)


# Endpoint for retrieving a single business
@router.get(
    "/businesses/{business_id}/",
    response_model=Union[ResponseBusiness, BusinessNotFound],
    status_code=status.HTTP_200_OK,
)
async def get_single_business(business_id: str, db: Session = Depends(get_db)):
    try:
        single_business = await query_single_business(db, business_id)

        if not single_business:
            not_found = BusinessNotFound(
                status=str(status.HTTP_404_NOT_FOUND),
                message=f"Business with id `{business_id}` not found",
            )
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content=not_found.model_dump_json(),
                media_type="application/json",
            )
        response_data = {
            "status": "200",
            "data": jsonable_encoder(single_business),
            "message": "Successful",
        }
        return Response(
            status_code=status.HTTP_200_OK,
            content=json.dumps(response_data),
            media_type="application/json",
        )
    except Exception as e:
        exception_handler(e)


# Endpoint for updating a business
@router.put(
    "/businesses/{business_id}/",
    dependencies=[Depends(JWTBearer())],
    response_model=Union[SaveResponse, BusinessNotFound],
    status_code=status.HTTP_200_OK,
)
async def update_a_business(
    business_id: str,
    business_to_update: ResponseBusiness,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    try:
        print("Token from header:", token)
        business_uuid = uuid.UUID(business_id)
        entry_to_update = (
            db.query(Business)
            .filter(Business.id == business_uuid and Business.is_deleted == False)
            .first()
        )

        if not entry_to_update:
            business_not_found = BusinessNotFound(
                message=f"Busineess entry with id {business_id} not found"
            )
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content=business_not_found.model_dump_json(),
                media_type="application/json",
            )

        uploaded_image_paths = []
        for base64_image in business_to_update.images:
            image_path = await upload_image(base64_image)
            uploaded_image_paths.append(image_path)

        entry_to_update.name = (business_to_update.name,)
        entry_to_update.handle = (business_to_update.handle,)
        entry_to_update.images = (uploaded_image_paths,)
        entry_to_update.location = (business_to_update.location,)
        entry_to_update.opening = (business_to_update.opening,)
        entry_to_update.business_description = (
            business_to_update.business_description,
        )
        entry_to_update.telephone_number = (business_to_update.telephone_number,)
        entry_to_update.category = (business_to_update.category,)
        entry_to_update.user_id = (business_to_update.user_id,)
        entry_to_update.created_at = (datetime.now(),)

        db.commit()
        response = SaveResponse(
            status=status.HTTP_200_OK,
            message=f"Business with id {business_id} updated successfully.",
        )
        return Response(
            content=response.json(),
            media_type="application/json",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        exception_handler(e)


# Endpoint for deleting a business
@router.delete(
    "/businesses/{business_id}/",
    dependencies=[Depends(JWTBearer())],
)
async def delete_a_business(
    business_id: str, db: Session = Depends(get_db), authorization: str = Header(None)
):
    try:
        token: str = (
            authorization.split(" ")[1]
            if authorization and " " in authorization
            else None
        )
        business_uuid = uuid.UUID(business_id)
        business_to_delete = (
            db.query(Business)
            .filter(Business.id == business_uuid and Business.is_deleted == False)
            .first()
        )

        if not business_to_delete:
            not_found = BusinessNotFound(
                message=f"Business with id {business_id} was not found",
            )
            return Response(
                content=not_found.model_dump_json(),
                media_type="application/json",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        user_info = get_user_from_token(token)

        if user_info["user_id"] != business_to_delete.user_id:
            delete_response = DeleteResource(
                status="403",
                message="You can only delete your Resource",
            )
            return Response(
                content=delete_response.model_dump_json(),
                media_type="application/json",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        # soft delete
        business_to_delete.is_deleted = True

        db.commit()
        response = SaveResponse(
            status=status.HTTP_200_OK,
            message=f"Business with id {business_id} was successfully deleted",
        )
        return Response(
            content=response.json(),
            media_type="application/json",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        exception_handler(e)


# Export the router
business_routes = router
