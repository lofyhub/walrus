from pydantic import BaseModel
from typing import Optional, List
from dataclasses import dataclass
from enum import Enum


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
    Nairobi_City = 'Nairobi City'



class UserPayload:
    fullname: str
    email: str
    picture: str

class BusinessPayload:
    name: str
    handle: str
    images: list[str]
    location: County
    opening: str
    business_description: str
    telephone_number: str
    category: str
    user_id: str

class ReviewPayload:
    user_id: str
    rating: int
    text: str
    image: List[str]
    business_id: str