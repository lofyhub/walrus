from pydantic import BaseModel, EmailStr, UUID4


class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True


class SQLAlchemyErrorMessage(OurBaseModel):
    detail: str = (
        "An error occurred while processing your request. Please try again later"
    )


class LoginPayload(OurBaseModel):
    fullname: str
    email: EmailStr


class UserSignup(OurBaseModel):
    id: UUID4
    name: str
    email: str
    tel_number: str
    picture: str


class SuccessResponse(OurBaseModel):
    status: str
    message: str
    user: UserSignup
    access_token: str
