from sqlalchemy.orm import Session


async def save_reviewed_business_to_db(db: Session, new_business):
    try:
        db.add(new_business)
        db.commit()
        db.refresh(new_business)
        return new_business
    except Exception as error:
        raise error


async def save_review_to_db(db: Session, new_business_review):
    try:
        db.add(new_business_review)
        db.commit()
    except Exception as error:
        raise error
