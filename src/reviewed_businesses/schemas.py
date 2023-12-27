from typing import List, Optional, Any, Annotated
from pydantic import BaseModel, UUID4
from enum import Enum
from fastapi import UploadFile, Form


class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True


class DefaultResponse(OurBaseModel):
    status: bool
    msg: str
    details: Optional[dict[Any, Any]] = {}


class SQLAlchemyErrorMessage(OurBaseModel):
    detail: str = (
        "An error occurred while processing your request. Please try again later"
    )


class County(Enum):
    Mombasa = "Mombasa"
    Kwale = "Kwale"
    Kilifi = "Kilifi"
    Tana_River = "Tana River"
    Lamu = "Lamu"
    Taita_Taveta = "Taita/Taveta"
    Garissa = "Garissa"
    Wajir = "Wajir"
    Mandera = "Mandera"
    Marsabit = "Marsabit"
    Isiolo = "Isiolo"
    Meru = "Meru"
    Tharaka_Nithi = "Tharaka-Nithi"
    Embu = "Embu"
    Kitui = "Kitui"
    Machakos = "Machakos"
    Makueni = "Makueni"
    Nyandarua = "Nyandarua"
    Nyeri = "Nyeri"
    Kirinyaga = "Kirinyaga"
    Muranga = "Murang'a"
    Kiambu = "Kiambu"
    Turkana = "Turkana"
    West_Pokot = "West Pokot"
    Samburu = "Samburu"
    Trans_Nzoia = "Trans Nzoia"
    Uasin_Gishu = "Uasin Gishu"
    Elgeyo_Marakwet = "Elgeyo/Marakwet"
    Nandi = "Nandi"
    Baringo = "Baringo"
    Laikipia = "Laikipia"
    Nakuru = "Nakuru"
    Narok = "Narok"
    Kajiado = "Kajiado"
    Kericho = "Kericho"
    Bomet = "Bomet"
    Kakamega = "Kakamega"
    Vihiga = "Vihiga"
    Bungoma = "Bungoma"
    Busia = "Busia"
    Siaya = "Siaya"
    Kisumu = "Kisumu"
    Homa_Bay = "Homa Bay"
    Migori = "Migori"
    Kisii = "Kisii"
    Nyamira = "Nyamira"
    Nairobi = "Nairobi"


def get_county_str(county: County) -> str:
    return county.value


class BusinessPayload(OurBaseModel):
    name: Annotated[str, Form(...)]
    county: Annotated[str, Form(...)]
    town: Annotated[str, Form(...)]
    category: Annotated[str, Form(...)]
    images: List[UploadFile] = Form(...)
    amenities: Annotated[List[str], Form(...)]
    star: Annotated[str, Form(...)]
    review: Annotated[str, Form(...)]


class UserReview(OurBaseModel):
    review: str
    business_id: str
    star: str


class ReviewResponse(OurBaseModel):
    status: str
    message: str


class ReviewBusiness(OurBaseModel):
    status: str
    message: str
