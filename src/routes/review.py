from fastapi import status, HTTPException, APIRouter, Response, Form, UploadFile
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal
from schema.schema import  SQLAlchemyErrorMessage, SaveResponse, ReviewResponse
from models.models import Review
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from auth.auth import get_user_from_token
from utils.helpers import upload_image

# Create a database session
db = SessionLocal()

# Create an API router
router = APIRouter()

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Endpoint for saving review
@router.post('/reviews/', response_model=SaveResponse, status_code=status.HTTP_201_CREATED)
async def save_review(
    images: List[UploadFile],
    text: Annotated[str, Form()],
    rating: Annotated[int, Form()],
    business_id: Annotated[str, Form()],
    user_id: Annotated[int, Form()],
    ):
    try:
        uploaded_image_paths = await upload_image(images)
        new_review = Review(
            images = uploaded_image_paths,
            text = text,
            rating = rating,
            business_id = business_id,
            user_id = user_id,
            created_at = datetime.now(),
        )

        db.add(new_review)
        db.commit()
        response = SaveResponse(status='Ok', message="Review successfully saved")
        return response
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)



# Endpoint for retrieving  reviews
@router.get('/reviews/', response_model=List[ReviewResponse], status_code=status.HTTP_200_OK)
async def get_reviews(skip: int = 0, limit: int = 100):
    try:
        # return none deleted users
        all_reviews: List[ReviewResponse] = db.query(Review).filter(Review.is_deleted == False).offset(skip).limit(limit).all()
        return all_reviews
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)



# Endpoint for updating a review
@router.put('/reviews/{review_id}/',response_model=SaveResponse, status_code=status.HTTP_200_OK)
async def update_a_review(review_id: int, review_to_update: ReviewResponse):
    try:
        entry_to_update = db.query(Review).filter(Review.id == review_id).first()

        if entry_to_update is None:
            raise HTTPException(status_code=400, detail=f"Review with id {review_id} was not found")
        
        entry_to_update.rating = review_to_update.rating
        entry_to_update.text = review_to_update.text
        entry_to_update.created_at = datetime.now()

        db.commit()
        response = SaveResponse(status='Ok', message=f"Review with id {review_id} updated successfully.")
        return Response(content=response.json(), media_type='application/json', status_code=status.HTTP_200_OK)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)



# Endpoint for deleting a review
@router.delete('/reviews/{review_id}/', response_model = SaveResponse, status_code=status.HTTP_200_OK)
async def delete_a_review(review_id: int):
    try:
        review_to_delete = db.query(Review).filter(Review.id == review_id).first()

        if review_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Review with id {review_id} was not found")
        
        # soft delete
        review_to_delete.is_deleted = True

        db.commit()
        response = SaveResponse(status='Ok', message=f"Review with id {review_id} was successfully deleted")
        return Response(content=response.json(), media_type='application/json', status_code=status.HTTP_200_OK)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)

# Export the router
reviews_routes = router