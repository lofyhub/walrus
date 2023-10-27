from .models import Review
from sqlalchemy.orm import Session, joinedload
import uuid


async def save_user_reviews(db: Session, new_review):
    try:
        db.add(new_review)
        db.commit()
    except Exception as error:
        raise error


async def query_reviews(db: Session, skip: int = 0, limit: int = 100):
    try:
        all_reviews = (
            db.query(Review)
            .filter(Review.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return all_reviews
    except Exception as error:
        raise error


async def query_business_reviews(db: Session, business_id: str):
    try:
        # TODO: implement pagination
        business_uuid = uuid.UUID(business_id)
        all_reviews = (
            db.query(Review)
            .filter(Review.business_id == business_uuid)
            .options(joinedload(Review.user))
            .all()
        )

        return all_reviews
    except Exception as error:
        raise error


async def query_single_reviews(db: Session, review_id: str):
    try:
        review_uuid = uuid.UUID(review_id)
        single_review = (
            db.query(Review)
            .filter(Review.id == review_uuid and Review.is_deleted == False)
            .first()
        )

        return single_review
    except Exception as error:
        raise error
