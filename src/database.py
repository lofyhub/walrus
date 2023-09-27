from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import MySQLdb
# Create an SQLAlchemy dialect for MySQLdb
from sqlalchemy.dialects.mysql import mysqldb

# Create a MySQLdb connection using MySQLdb.connect
connection = MySQLdb.connect(
    host=settings.DB_HOST,
    user=settings.DB_USERNAME,
    passwd=settings.DB_PASSWORD,
    db=settings.DB_NAME,
    autocommit=True,
    ssl_mode = "DISABLED",
)


engine = create_engine("mysql+mysqldb://", creator=lambda: connection, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = Base.metadata

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()