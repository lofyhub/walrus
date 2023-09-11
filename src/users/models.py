from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
from utils import gen_uuid
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(String(255), primary_key=True, default=gen_uuid)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    picture = Column(String(255), nullable=False)
    tel_number = Column(String(10), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    reviews = relationship("Review", back_populates="user")
    businesses = relationship("Business", back_populates="user")
