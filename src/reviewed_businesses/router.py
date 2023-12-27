from fastapi import status, APIRouter, Depends, Header, UploadFile, Form
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from database import get_db
from .schemas import ReviewResponse
from auth.auth_bearer import JWTBearer
from .services import (
    save_reviewed_business_to_db,
    save_review_to_db,
)
from businesses.error_handler import exception_handler
from auth.auth import get_user_from_token
from utils import upload_image
from businesses.models import Business
from reviews.models import Review
import uuid
from typing import Annotated, List


# Create an API router
router = APIRouter()

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Endpoint for saving a reviewed business
@router.post("/reviewed_businesses/", dependencies=[Depends(JWTBearer())])
async def save_reviewed_business(
    images: List[UploadFile],
    name: Annotated[str, Form(...)],
    county: Annotated[str, Form(...)],
    town: Annotated[str, Form(...)],
    category: Annotated[str, Form(...)],
    review: Annotated[str, Form(...)],
    star: Annotated[str, Form(...)],
    amenities: Annotated[List[str], Form()],
    db=Depends(get_db),
    authorization: str = Header(None),
):
    try:
        token: str = (
            authorization.split(" ")[1]
            if authorization and " " in authorization
            else None
        )

        user_id = get_user_from_token(token)["user_id"]

        images_paths = await upload_image(images)

        new_business = Business(
            name=name,
            handle=name,
            images=images_paths,
            location=town,
            county=county,
            town=town,
            opening_hours=["8:00", "17:00"],
            business_description="This businesss has no description yet",
            telephone_number="0712345678",
            category=category,
            user_id=uuid.UUID(user_id),
            amenities=amenities,
            verified=False,
        )
        res_business = await save_reviewed_business_to_db(db, new_business)

        user_review = Review(
            images=images_paths,
            text=review,
            rating=int(star),
            business_id=res_business.id,
            user_id=uuid.UUID(user_id),
        )

        await save_review_to_db(db, user_review)

        response_data = ReviewResponse(
            status=str(status.HTTP_201_CREATED),
            message="Business Review successfully saved",
        )
        return JSONResponse(
            content=response_data.model_dump(), status_code=status.HTTP_201_CREATED
        )
    except Exception as error:
        exception_handler(error)


# Export the router
reviewed_business_routes = router
