from fastapi import (
    status,
    HTTPException,
    APIRouter,
    Response,
    Form,
    UploadFile,
    Depends,
    Header,
)
from typing import Annotated, Union, Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from database import get_db
from .schemas import SQLAlchemyErrorMessage, SaveResponse, ReviewResponse, UpdateReview
from .models import Review
from users.models import User
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from utils import upload_image
from auth.auth_bearer import JWTBearer
from .exceptions import exception_handler
from .services import save_user_reviews, query_reviews, query_business_reviews
from auth.auth import get_user_from_token
import uuid

# Create an API router
router = APIRouter()

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Endpoint for saving review
@router.post(
    "/reviews/",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED,
)
async def save_review(
    text: Annotated[str, Form()],
    rating: Annotated[str, Form()],
    business_id: Annotated[str, Form()],
    user_id: Annotated[str, Form()],
    images: Union[UploadFile, List[UploadFile], None] = None,
    db=Depends(get_db),
):
    try:
        uploaded_image_paths = []
        if images is not None:
            uploaded_image_paths = await upload_image(images)
        new_review = Review(
            images=uploaded_image_paths,
            text=text,
            rating=int(rating),
            business_id=uuid.UUID(business_id),
            user_id=uuid.UUID(user_id),
        )
        await save_user_reviews(db, new_review)

        response_data = SaveResponse(status="201", message="Review successfully saved")

        return JSONResponse(
            content=response_data.model_dump(), status_code=status.HTTP_201_CREATED
        )
    except Exception as error:
        exception_handler(error)


# Endpoint for retrieving  reviews
@router.get(
    "/reviews/",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
)
async def get_reviews(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    try:
        # return none deleted reviews
        all_reviews = await query_reviews(db, skip, limit)
        serialized_reviews = []
        for review in all_reviews:
            serialized_review = {
                "id": review.id,
                "rating": review.rating,
                "text": review.text,
                "images": review.images,
                "user": {
                    "full_name": review.user.name,
                    "photo": review.user.picture,
                },
                "user_id": review.user_id,
                "business_id": review.business_id,
                "created_at": review.created_at,
            }
            serialized_reviews.append(serialized_review)
        return ReviewResponse(
            status=str(status.HTTP_200_OK),
            data=serialized_reviews,
            reviews=len(serialized_reviews),
        )
    except Exception as error:
        exception_handler(error)


# Endpoint for retrieving reviews for a given business
@router.get(
    "/review/{business_id}",
)
async def get_single_reviews(
    business_id: str,
    db=Depends(get_db),
):
    try:
        # return all reviews for a business
        business_reviews = await query_business_reviews(db, business_id)

        if not business_reviews:
            return JSONResponse(
                content={
                    "status": "200",
                    "message": f"Reviews for Business with id: `{business_id}` not found",
                },
                status_code=status.HTTP_200_OK,
            )
        serialized_reviews = []

        for review in business_reviews:
            # TODO: their is a better way to do this than converting strings
            # For now just using str -> Object of type UUID is not JSON serializable
            serialized_review = {
                "id": str(review.id),
                "rating": review.rating,
                "text": review.text,
                "images": review.images,
                "user": {
                    "full_name": review.user.name,
                    "photo": review.user.picture,
                },
                "user_id": str(review.user_id),
                "business_id": str(review.business_id),
                "created_at": str(review.created_at),
            }
            serialized_reviews.append(serialized_review)

        return JSONResponse(
            content={
                "status": "200",
                "data": serialized_reviews,
                "message": "Succesful",
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as error:
        exception_handler(error)


# Endpoint for updating a review
@router.put(
    "/reviews/{review_id}/",
    dependencies=[Depends(JWTBearer())],
    response_model=SaveResponse,
    status_code=status.HTTP_200_OK,
)
async def update_a_review(
    review_id: str,
    review_to_update: UpdateReview,
    db=Depends(get_db),
    authorization: str = Header(None),
):
    try:
        review_uuid = uuid.UUID(review_id)

        entry_to_update = db.query(Review).filter(Review.id == review_uuid).first()

        if entry_to_update is None:
            raise HTTPException(
                status_code=400, detail=f"Review with id {review_id} was not found"
            )

        token = (
            authorization.split(" ")[1]
            if authorization and " " in authorization
            else None
        )

        user_id_from_token = get_user_from_token(token)

        if user_id_from_token["user_id"] != entry_to_update.user_id:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "status": "403",
                    "message": "You can only update your resource",
                },
            )

        entry_to_update.rating = int(review_to_update.rating)
        entry_to_update.text = review_to_update.text
        entry_to_update.created_at = datetime.now()

        db.commit()
        response = SaveResponse(
            status="Ok", message=f"Review with id {review_id} updated successfully."
        )
        return Response(
            content=response.json(),
            media_type="application/json",
            status_code=status.HTTP_200_OK,
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SQLAlchemyErrorMessage,
        )


# Endpoint for deleting a review
@router.delete(
    "/reviews/{review_id}/",
    dependencies=[Depends(JWTBearer())],
)
async def delete_a_review(
    review_id: str, db=Depends(get_db), authorization: str = Header(None)
):
    try:
        token = (
            authorization.split(" ")[1]
            if authorization and " " in authorization
            else None
        )
        review_uuid = uuid.UUID(review_id)
        review_to_delete = db.query(Review).filter(Review.id == review_uuid).first()

        if not review_to_delete:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "status": "404",
                    "message": f"Review with id `{review_id}` was not found",
                },
            )

        user_info_from_token = get_user_from_token(token)

        if user_info_from_token["user_id"] != review_to_delete.user_id:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "status": "403",
                    "message": "You can only delete your resource",
                },
            )

        # soft delete
        review_to_delete.is_deleted = True

        db.commit()
        response = SaveResponse(
            status="Ok", message=f"Review with id {review_id} was successfully deleted"
        )
        return Response(
            content=response.model_dump_json(),
            media_type="application/json",
            status_code=status.HTTP_200_OK,
        )
    except Exception as error:
        exception_handler(error)


# Export the router
reviews_routes = router
