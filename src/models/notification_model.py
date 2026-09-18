from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base_model import Base
from src.models.notification_enums import NotificationChannel, NotificationStatus


class Notification(Base):
    """Model for entity <Notification>."""

    __tablename__ = "notifications"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[NotificationChannel] = mapped_column(
        String(50), index=True, nullable=False
    )
    status: Mapped[NotificationStatus] = mapped_column(
        String(50), index=True, default=NotificationStatus.PENDING, nullable=False
    )
