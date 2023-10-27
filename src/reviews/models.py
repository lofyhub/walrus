from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship, mapped_column
from database import Base
from utils import gen_uuid
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID


class Review(Base):
    __tablename__ = "reviews"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=gen_uuid)
    user_id = mapped_column(UUID(as_uuid=True), nullable=False)
    rating = mapped_column(Integer, nullable=False)
    text = mapped_column(Text, nullable=False)
    images = mapped_column(MutableList.as_mutable(PickleType), nullable=False)
    business_id = mapped_column(UUID(as_uuid=True), nullable=False)
    is_deleted = mapped_column(Boolean, nullable=False, default=False)
    created_at = mapped_column(DateTime, nullable=False, default=datetime.now())

    user = relationship(
        "User",
        back_populates="reviews",
        primaryjoin="foreign(Review.user_id) == User.id",
    )
    business = relationship(
        "Business",
        back_populates="reviews",
        primaryjoin="foreign(Review.business_id) == Business.id",
    )
