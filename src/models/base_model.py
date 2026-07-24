from datetime import datetime
from typing import Annotated
import uuid
from sqlalchemy import func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.models.db_types import id_pk, timestamp_created, timestamp_updated


class Base(DeclarativeBase):
    """Base model class. Will be inherited by all other entities."""

    id: Mapped[id_pk]
    created_at: Mapped[timestamp_created]
    updated_at: Mapped[timestamp_updated]
