from pydantic import BaseModel, UUID4
from typing import List
from dataclasses import dataclass
from datetime import datetime

 
class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True

class SQLAlchemyErrorMessage(OurBaseModel):
    detail:str = "An error occurred while processing your request. Please try again later"

class ReviewPayload(OurBaseModel):
    user_id: UUID4
    rating: int
    text: str
    images: List[str]
    business_id: UUID4

class User(OurBaseModel):
      full_name: str
      photo: str
class Reviews(OurBaseModel):
    id: UUID4
    rating: int
    business_id: UUID4
    user_id: UUID4
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