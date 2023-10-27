from fastapi import UploadFile
from pydantic import BaseModel, EmailStr


class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True


class ImageFile(OurBaseModel):
    filename: str
    content_type: str
    file: UploadFile


class UserPayload(OurBaseModel):
    fullname: str
    email: EmailStr
    tel_number: str
    picture: str


class SQLAlchemyErrorMessage(OurBaseModel):
    detail: str = (
        "An error occurred while processing your request. Please try again later"
    )
