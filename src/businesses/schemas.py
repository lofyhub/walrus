from typing import List, Optional, Any
from pydantic import BaseModel, UUID4
from enum import Enum
from datetime import datetime


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
    name: str
    handle: str
    images: List[str]
    location: County
    opening_hours: List[str]
    business_description: str
    telephone_number: str
    category: str
    amenities: List[str]
    user_id: str


class ResponseBusiness(OurBaseModel):
    id: UUID4
    name: str
    handle: str
    location: str
    town: str
    county: str
    verified: bool
    category: str
    user_id: UUID4
    business_description: str
    opening_hours: List[str]
    amenities: List[str]
    images: List[str]
    created_at: datetime


class SaveResponse(OurBaseModel):
    status: str
    message: str


class QuerySuccess(OurBaseModel):
    data: list[ResponseBusiness]
    businesses: str


class GetBusinesses(OurBaseModel):
    status: str
    data: list[ResponseBusiness]
    businesses: str


class BusinessNotFound(OurBaseModel):
    status: str = "404"
    message: str = "No businesses was found"
    businesses: Optional[str] = None


class DeleteResource(OurBaseModel):
    status: str
    message: str
