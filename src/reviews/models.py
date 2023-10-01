from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
from utils import gen_uuid
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from datetime import datetime

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), nullable=False)
    rating = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    images = Column(MutableList.as_mutable(PickleType), default=[], nullable=False)
    business_id = Column(String(36), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    
    user = relationship("User", back_populates="reviews")
    business = relationship("Business", back_populates="reviews")

