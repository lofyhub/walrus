from database import Base,engine
from businesses.models import Business
from reviews.models import Review
from users.models import User

print("Creating database ....")

Base.metadata.create_all(engine);