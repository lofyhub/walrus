from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from utils import gen_uuid
from datetime import datetime

class Business(Base):
    __tablename__ = 'businesses'
    id = Column(String(36), primary_key=True, default=gen_uuid)
    name = Column(String(255), nullable=False)
    handle = Column(String(255), nullable=False)
    images = Column(MutableList.as_mutable(PickleType), default=[], nullable=False)
    location = Column(String(255), nullable=False)
    county = Column(String(255), nullable=False)
    town = Column(String(255), nullable=False)
    opening_hours = Column(MutableList.as_mutable(PickleType), nullable=False)
    business_description = Column(String(255), nullable=False)
    verified = Column(Boolean, nullable=False)
    telephone_number = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    amenities = Column(MutableList.as_mutable(PickleType), default=[], nullable=False)
    user_id = Column(String(36), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    user = relationship("User", back_populates="businesses")
    reviews = relationship("Review", back_populates="business")