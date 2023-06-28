from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    picture = Column(String(255))
    created_at = Column(DateTime)

    businesses = relationship("Business", back_populates="user")


class Business(Base):
    __tablename__ = 'businesses'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    handle = Column(String(255))
    reviews = Column(Integer)
    review_score = Column(Float)
    location = Column(String(255))
    opening = Column(Boolean)
    business_description = Column(Text)
    creation_date = Column(String(255))
    verified = Column(Boolean)
    telephone_number = Column(String(255))
    category = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="businesses")

    reviews = relationship("Review", back_populates="business")


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    rating = Column(Integer)
    created_at = Column(DateTime)
    text = Column(Text)
    image = Column(String(255))
    business_id = Column(Integer, ForeignKey('businesses.id'))

    business = relationship("Business", back_populates="reviews")
