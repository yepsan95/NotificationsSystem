from datetime import datetime
from typing import Annotated
import uuid
from sqlalchemy import func, text, inspect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.models.db_types import id_pk, timestamp_created, timestamp_updated


class Base(DeclarativeBase):
    """Base model class. Will be inherited by all other entities."""

    id: Mapped[id_pk]
    created_at: Mapped[timestamp_created]
    updated_at: Mapped[timestamp_updated]

    def to_dict(self):
        obj_dict = {
            c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs
        }
        obj_dict["id"] = str(self.id)
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict
