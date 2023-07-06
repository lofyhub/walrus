from fastapi import UploadFile
from pydantic import BaseModel


class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True

class ImageFile(OurBaseModel):
    filename: str
    content_type: str
    file: UploadFile



class SQLAlchemyErrorMessage(OurBaseModel):
    detail:str = "An error occurred while processing your request. Please try again later"
