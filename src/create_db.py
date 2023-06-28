from database.database import Base,engine
from models.models import User, Business, Review

print("Creating database ....")

Base.metadata.create_all(engine);