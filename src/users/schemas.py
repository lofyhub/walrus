from pydantic import BaseModel, EmailStr
from dataclasses import dataclass
from datetime import datetime


class OurBaseModel(BaseModel):
    class Config: 
        orm_mode = True

class SQLAlchemyErrorMessage(OurBaseModel):
    detail:str = "An error occurred while processing your request. Please try again later"

class UserPayload(OurBaseModel):
    fullname: str
    email: EmailStr
    tel_number: str
    picture: str

class UserResponse(OurBaseModel):
    id: str
    name: str
    email: EmailStr
    tel_number: str
    picture: str
    created_at: datetime

class SaveResponse(OurBaseModel):
    status: str
    message: str