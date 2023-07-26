from pydantic import BaseModel, EmailStr


class OurBaseModel(BaseModel):
    class Config: 
        orm_mode = True

class SQLAlchemyErrorMessage(OurBaseModel):
    detail:str = "An error occurred while processing your request. Please try again later"

class LoginPayload(OurBaseModel):
    fullname: str
    email: EmailStr

class SuccessResponse(OurBaseModel):
    status: str
    message: str
    access_token: str