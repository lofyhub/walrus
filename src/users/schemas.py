from pydantic import BaseModel, EmailStr, UUID4
from dataclasses import dataclass
from datetime import datetime


class OurBaseModel(BaseModel):
    class Config: 
        from_attributes = True

class SQLAlchemyErrorMessage(OurBaseModel):
    detail:str = "An error occurred while processing your request. Please try again later"

class UserPayload(OurBaseModel):
    fullname: str
    email: EmailStr
    tel_number: str
    picture: str

class SaveUser(OurBaseModel):
    name: str
    email: EmailStr
    picture: str
    tel_number: str


class LoginPayload(OurBaseModel):
    fullname: str
    email: EmailStr


class UserResponse(OurBaseModel):
    id: UUID4
    name: str
    email: EmailStr
    picture: str
    is_deleted: bool
    tel_number: str
    created_at: datetime

class GetUser(OurBaseModel):
    status: str
    data: list[UserResponse]
    users: int

class UserData(OurBaseModel):
    id: UUID4
    name: str
    email: str
    tel_number: str
    picture: str
    access_token: str
class SaveResponse(OurBaseModel):
    status: str
    message: str
    user: UserData
