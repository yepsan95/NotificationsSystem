from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.models.notification_enums import NotificationChannel, NotificationStatus
from src.schemas.base_schema import BaseResponse


class NotificationResponse(BaseResponse):
    """Response schema for <Notification> endpoints."""

    user_id: UUID
    title: str
    content: str
    channel: NotificationChannel
    status: NotificationStatus


class NotificationCreate(BaseModel):
    """Request schema for <Notification> POST and PUT endpoints."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(
        ..., min_length=1, max_length=255, description="Notification title."
    )
    content: str = Field(
        ..., min_length=1, description="Body content of the notification."
    )
    channel: NotificationChannel = Field(
        ..., description="Delivery channel (EMAIL, SMS, PUSH)."
    )


class NotificationUpdate(BaseModel):
    """Request schema for <Notification> PATCH endpoints."""

    model_config = ConfigDict(str_strup_whitespaces=True)

    title: str | None = None
    content: str | None = None
    channel: NotificationChannel | None = None
    status: NotificationStatus | None = None
