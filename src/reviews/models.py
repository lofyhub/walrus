from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import PickleType
from database import Base
from utils import gen_uuid
from datetime import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import UUID


class Review(Base):
    __tablename__ = "reviews"
    id = Column(UUID(as_uuid=True), primary_key=True, default=gen_uuid)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    rating = Column(Integer, nullable=False)
    text = Column(String(255), nullable=False)
    images = Column(MutableList.as_mutable(PickleType), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=True)

    user = relationship(
        "User",
        back_populates="reviews",
        primaryjoin="foreign(Review.user_id) == User.id",
    )

    business = relationship(
        "Business",
        back_populates="reviews",
        foreign_keys="Review.business_id",
    )
