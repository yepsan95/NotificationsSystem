from datetime import datetime
from uuid import UUID
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from src.models.base_model import Base


class User(Base):
    """Model for entity <User>."""

    __tablename__ = "users"
    
    first_name: Mapped[str] = mapped_column(index=True, nullable=False)
    middle_name: Mapped[str] = mapped_column(index=True, nullable=True)
    last_name: Mapped[str] = mapped_column(index=True, nullable=False)
    email: Mapped[str] = mapped_column(index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
