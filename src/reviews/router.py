from fastapi import status, HTTPException, APIRouter, Response, Form, UploadFile, Depends
from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from .schemas import  SQLAlchemyErrorMessage, SaveResponse, ReviewResponse
from .models import Review
from users.models import User
from datetime import datetime
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from utils import upload_image
from auth.auth_bearer import JWTBearer

# Create a database session
db = SessionLocal()

# Create an API router
router = APIRouter()

# Define the OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Endpoint for saving review
@router.post('/reviews/',dependencies=[Depends(JWTBearer())], response_model=SaveResponse, status_code=status.HTTP_201_CREATED)
async def save_review(
    text: Annotated[str, Form()],
    rating: Annotated[str, Form()],
    business_id: Annotated[str, Form()],
    user_id: Annotated[str, Form()],
    images: Optional[List[UploadFile]] = None,
    ):
    try:

        uploaded_image_paths = []
        if images:
            uploaded_image_paths = await upload_image(images)
        
        new_review = Review(
            images = uploaded_image_paths,
            text = text,
            rating = int(rating),
            business_id = business_id,
            user_id = user_id,
        )

        db.add(new_review)
        db.commit()
        response = SaveResponse(status='201', message="Review successfully saved")
        return response
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)



# Endpoint for retrieving  reviews
@router.get('/reviews/', response_model=ReviewResponse, status_code=status.HTTP_200_OK)
async def get_reviews(skip: int = 0, limit: int = 100):
    try:
        # return none deleted users
        all_reviews = db.query(Review).join(User).filter(Review.is_deleted == False).offset(skip).limit(limit).all()
        serialized_reviews = []
        print(all_reviews)
        for review in all_reviews:
            serialized_review = {
                'id': review.id,
                'user_id': review.user_id,
                'business_id': review.business_id,
                'rating': review.rating,
                'text': review.text,
                'images': review.images, 
                'user':{
                    'full_name': review.user.name,
                    'photo': review.user.picture,
                },
                'created_at': review.created_at,
            }
            serialized_reviews.append(serialized_review)
        response = ReviewResponse(status= str(status.HTTP_200_OK), data= serialized_reviews, reviews= len(serialized_reviews))
        return response
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)


# Endpoint for retrieving a single review
@router.get('/reviews/{business_id}', response_model=ReviewResponse, status_code=status.HTTP_200_OK)
async def get_single_reviews(business_id: str):
    try:
        # return a single review
        business_reviews: ReviewResponse= db.query(Review).join(User).filter(Review.business_id == business_id).all()

        if business_reviews is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Business reviews for {business_id} not found")
        
        serialized_reviews = []
        
        for review in business_reviews:
            serialized_review = {
                'id': review.id,
                'user_id': review.user_id,
                'business_id': review.business_id,
                'rating': review.rating,
                'text': review.text,
                'images': review.images,
                'user':{
                    'full_name': review.user.name,
                    'photo': review.user.picture,
                },
                'created_at': review.created_at,
            }
            serialized_reviews.append(serialized_review)
        
        response = ReviewResponse(status= str(status.HTTP_200_OK), data= serialized_reviews, reviews= len(serialized_reviews))
        return response
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SQLAlchemyErrorMessage)



# Endpoint for updating a review
@router.put('/reviews/{review_id}/', dependencies=[Depends(JWTBearer())], response_model=SaveResponse, status_code=status.HTTP_200_OK)
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
@router.delete('/reviews/{review_id}/', dependencies=[Depends(JWTBearer())], response_model = SaveResponse, status_code=status.HTTP_200_OK)
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