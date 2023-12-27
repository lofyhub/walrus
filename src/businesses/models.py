from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import relationship, mapped_column
from database import Base
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from utils import gen_uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID


class Business(Base):
    __tablename__ = "businesses"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=gen_uuid)
    name = mapped_column(String(255), nullable=False)
    handle = mapped_column(String(255), nullable=False)
    images = mapped_column(
        MutableList.as_mutable(PickleType), default=[], nullable=False
    )
    location = mapped_column(String(255), nullable=False)
    county = mapped_column(String(255), nullable=False)
    town = mapped_column(String(255), nullable=False)
    opening_hours = mapped_column(MutableList.as_mutable(PickleType), nullable=False)
    business_description = mapped_column(String(255), nullable=False)
    verified = mapped_column(Boolean, nullable=False)
    telephone_number = mapped_column(String(255), nullable=False)
    category = mapped_column(String(255), nullable=False)
    amenities = mapped_column(
        MutableList.as_mutable(PickleType), default=[], nullable=False
    )
    user_id = mapped_column(UUID(as_uuid=True), nullable=False)
    is_deleted = mapped_column(Boolean, nullable=False, default=False)
    created_at = mapped_column(DateTime, nullable=False, default=datetime.now())

    user = relationship(
        "User",
        back_populates="businesses",
        primaryjoin="foreign(Business.user_id) == User.id",
    )
    reviews = relationship(
        "Review",
        back_populates="business",
        primaryjoin="Business.id == foreign(Review.business_id)",
    )
