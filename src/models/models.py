from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.database import Base
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    picture = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)

    businesses = relationship("Business", back_populates="user")


class Business(Base):
    __tablename__ = 'businesses'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    handle = Column(String(255), nullable=False)
    images = Column(MutableList.as_mutable(PickleType),default=[], nullable=False)
    location = Column(String(255), nullable=False)
    opening_hours = Column(MutableList.as_mutable(PickleType), nullable=False)
    business_description = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    verified = Column(Boolean, nullable=False)
    telephone_number = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    amenities = Column(MutableList.as_mutable(PickleType),default=[], nullable=False)
    user_id= Column(Integer, ForeignKey('users.id'), nullable=False)
    
    user = relationship("User", back_populates="businesses")
    reviews = relationship("Review", back_populates="business")


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    text = Column(Text, nullable=False)
    images = Column(MutableList.as_mutable(PickleType),default=[], nullable=False)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)

    business = relationship("Business", back_populates="reviews")
