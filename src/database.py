from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

MySQL_DATABASE_URL = settings.MySQL_DATABASE_URL
engine = create_engine(MySQL_DATABASE_URL, echo=True)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = Base.metadata


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
