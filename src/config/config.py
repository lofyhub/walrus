from pydantic import BaseSettings
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv(".env")

class Settings(BaseSettings):
    app_name: str = "WALRUS_API"
    CLOUDINARY_API_ID: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_URL: str
    JWT_SECRET:str
    JWT_ALGORITHM:str
    PORT: str
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()