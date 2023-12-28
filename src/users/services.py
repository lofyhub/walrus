from .models import User
from sqlalchemy.orm import Session
from .schemas import UserPayload
import uuid


def save_user_to_db(db: Session, user_payload: UserPayload):
    try:
        new_user = User(
            name=user_payload.fullname,
            email=user_payload.email,
            picture=user_payload.picture,
            tel_number=user_payload.tel_number,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as error:
        raise error


def query_user_by_email(db: Session, user_payload: UserPayload):
    try:
        user_exists = db.query(User).filter(User.email == user_payload.email).first() is not None
        return user_exists
    except Exception as error:
        raise error


def query_user_by_number(db: Session, user_payload: UserPayload):
    try:
        check_tel_number = (
            db.query(User).filter(User.tel_number == user_payload.tel_number).first()
        )
        return check_tel_number is not None
    except Exception as error:
        raise error


async def query_users(db: Session, skip: int, limit: int):
    try:
        all_users = (
            db.query(User)
            .filter(User.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return all_users
    except Exception as error:
        raise error


async def query_user(db: Session, user_id: str):
    try:
        user_uuid = uuid.UUID(user_id)
        user = (
            db.query(User)
            .filter(User.id == user_uuid, User.is_deleted == False)
            .first()
        )
        return user
    except Exception as error:
        raise error
