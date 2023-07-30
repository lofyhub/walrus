from pydantic import BaseModel
from typing import List
from dataclasses import dataclass
from datetime import datetime

 
class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True

class SQLAlchemyErrorMessage(OurBaseModel):
    detail:str = "An error occurred while processing your request. Please try again later"

class ReviewPayload(OurBaseModel):
    user_id: str
    rating: int
    text: str
    images: List[str]
    business_id: str

class User(OurBaseModel):
      full_name: str
      photo: str
class Reviews(OurBaseModel):
    id: str
    rating: int
    business_id: str
    user_id: str
    text: str
    images: List[str]
    user: User
    created_at: datetime
class ReviewResponse(OurBaseModel):
    status: str
    data: List[Reviews]
    reviews: int


class SaveResponse(OurBaseModel):
    status: str
    message: str