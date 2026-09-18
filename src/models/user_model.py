from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base_model import Base


class User(Base):
    """Model for entity <User>."""

    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(index=True, nullable=False)
    middle_name: Mapped[str] = mapped_column(index=True, nullable=True)
    last_name: Mapped[str] = mapped_column(index=True, nullable=False)
    email: Mapped[str] = mapped_column(index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str | None] = mapped_column(
        String(20), index=True, nullable=True
    )
    device_token: Mapped[str | None] = mapped_column(
        String(255), index=True, nullable=True
    )

    def get_safe_attributes(self):
        safe_attributes = self.to_dict()
        del safe_attributes["password_hash"]

        return safe_attributes
