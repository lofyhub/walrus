from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLITE_DATABASE_URL = "sqlite:///./kikao_database.db"
MySQL_DATABASE_URL = "mysql://root:Monica_7029@127.0.0.1/kikao_db" 


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
