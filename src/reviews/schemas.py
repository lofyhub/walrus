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

class ReviewResponse(OurBaseModel):
    id: str
    rating: int
    business_id: str
    user_id: str
    text: str
    images: List[str]
    created_at: datetime

class SaveResponse(OurBaseModel):
    status: str
    message: str