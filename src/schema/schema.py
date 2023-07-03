from fastapi import UploadFile
from pydantic import BaseModel, Field, constr
from typing import List
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True

class ImageFile(OurBaseModel):
    filename: str
    content_type: str
    file: UploadFile

class SaveResponse(OurBaseModel):
    status: str
    message: str


class SQLAlchemyErrorMessage(OurBaseModel):
    detail:str = "An error occurred while processing your request. Please try again later"

class County(Enum):
    Mombasa = 'Mombasa'
    Kwale = 'Kwale'
    Kilifi = 'Kilifi'
    Tana_River = 'Tana River'
    Lamu = 'Lamu'
    Taita_Taveta = 'Taita/Taveta'
    Garissa = 'Garissa'
    Wajir = 'Wajir'
    Mandera = 'Mandera'
    Marsabit = 'Marsabit'
    Isiolo = 'Isiolo'
    Meru = 'Meru'
    Tharaka_Nithi = 'Tharaka-Nithi'
    Embu = 'Embu'
    Kitui = 'Kitui'
    Machakos = 'Machakos'
    Makueni = 'Makueni'
    Nyandarua = 'Nyandarua'
    Nyeri = 'Nyeri'
    Kirinyaga = 'Kirinyaga'
    Muranga = 'Murang\'a'
    Kiambu = 'Kiambu'
    Turkana = 'Turkana'
    West_Pokot = 'West Pokot'
    Samburu = 'Samburu'
    Trans_Nzoia = 'Trans Nzoia'
    Uasin_Gishu = 'Uasin Gishu'
    Elgeyo_Marakwet = 'Elgeyo/Marakwet'
    Nandi = 'Nandi'
    Baringo = 'Baringo'
    Laikipia = 'Laikipia'
    Nakuru = 'Nakuru'
    Narok = 'Narok'
    Kajiado = 'Kajiado'
    Kericho = 'Kericho'
    Bomet = 'Bomet'
    Kakamega = 'Kakamega'
    Vihiga = 'Vihiga'
    Bungoma = 'Bungoma'
    Busia = 'Busia'
    Siaya = 'Siaya'
    Kisumu = 'Kisumu'
    Homa_Bay = 'Homa Bay'
    Migori = 'Migori'
    Kisii = 'Kisii'
    Nyamira = 'Nyamira'
    Nairobi = 'Nairobi'

def get_county_str(county: County) -> str:
    return county.value


class UserPayload(OurBaseModel):
    fullname: str
    email: str
    picture: str

class BusinessPayload(OurBaseModel):
    name: str
    handle: str
    images: list[str]
    location: County
    opening_hours: list[str]
    business_description: str
    telephone_number: str
    category: str
    amenities: List[str]
    user_id: str

class BusinessPayloadd(OurBaseModel):
    name: str
    handle: str
    images: list[str]
    location: County
    opening_hours: list[str]
    business_description: str
    telephone_number: str
    category: str
    user_id: str
    amenities: List[str]
    created_at: str

class ResponseBusiness(OurBaseModel):
    id: int
    name: str
    handle: str
    location: str
    verified: bool
    telephone_number: str
    category: str
    user_id: int
    business_description: str
    opening_hours: List[str]
    amenities: List[str]
    images: List[str]
    created_at: datetime

class ReviewPayload(OurBaseModel):
    user_id: str
    rating: int
    text: str
    images: List[str]
    business_id: str

class ReviewResponse(OurBaseModel):
    id: int
    rating: int
    business_id: str
    user_id: str
    text: str
    images: List[str]
    created_at: datetime

class OkResponse(OurBaseModel):
    status: str
    data: List[ResponseBusiness]