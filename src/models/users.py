from datetime import datetime, UTC, date

from sqlalchemy import Column, String, Boolean, ForeignKey, Date, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from database.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    birth_date: Mapped[date] = mapped_column(Date, nullable=True)
    phone_number: Mapped[str] = mapped_column(String(10), nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )
