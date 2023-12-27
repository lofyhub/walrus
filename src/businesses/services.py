from .models import Business
from sqlalchemy.orm import Session
import uuid


async def save_business_db(db: Session, new_business):
    try:
        db.add(new_business)
        db.commit()
    except Exception as error:
        raise error


async def query_businesses(db: Session, skip: int = 0, limit: int = 100):
    try:
        all_businesses = (
            db.query(Business)
            .filter(Business.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return all_businesses
    except Exception as error:
        raise error


async def query_single_business(db: Session, business_id: str):
    try:
        business_uuid = uuid.UUID(business_id)
        single_business = (
            db.query(Business)
            .filter(Business.id == business_uuid and Business.is_deleted == False)
            .first()
        )

        return single_business
    except Exception as error:
        print(error)
        raise error
