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

class LoginPayload(OurBaseModel):
    fullname: str
    email: EmailStr


class UserResponse(OurBaseModel):
    id: str
    name: str
    email: EmailStr
    picture: str
    created_at: datetime

class User(OurBaseModel):
    id: str
    name: str
    email: str
    tel_number: str
    picture: str
class SaveResponse(OurBaseModel):
    status: str
    message: str
    access_token: str
    user: User