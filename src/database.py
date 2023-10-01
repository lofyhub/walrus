from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

MySQL_DATABASE_URL = settings.MySQL_DATABASE_URL

engine = create_engine( MySQL_DATABASE_URL, echo=True)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = Base.metadata
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
