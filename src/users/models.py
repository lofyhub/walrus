from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship, mapped_column
from database import Base
from utils import gen_uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=gen_uuid)
    name = mapped_column(String(255), nullable=False)
    email = mapped_column(String(255), nullable=False)
    picture = mapped_column(String(255), nullable=False)
    tel_number = mapped_column(String(10), nullable=False)
    is_deleted = mapped_column(Boolean, nullable=False, default=False)
    created_at = mapped_column(DateTime, nullable=False, default=datetime.now())
    reviews = relationship(
        "Review",
        back_populates="user",
        primaryjoin="User.id == foreign(Review.user_id)",
    )
    businesses = relationship(
        "Business",
        back_populates="user",
        primaryjoin="User.id == foreign(Business.user_id)",
    )
