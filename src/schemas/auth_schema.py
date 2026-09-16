from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RefreshTokenCreate(BaseModel):
    """Create schema for <RefreshToken> entity."""

    model_config = ConfigDict(str_strip_whitespace=True)

    token: str
    user_id: UUID
    expires_at: datetime
    is_revoked: bool = Field(default=False)


class RefreshTokenUpdate(BaseModel):
    """Update schema for <RefreshToken> entity."""

    model_config = ConfigDict(str_strip_whitespace=True)

    token: str | None = None
    user_id: UUID | None = None
    expires_at: datetime | None = None
    is_revoked: bool | None = Field(default=False)


class LoginRequest(BaseModel):
    """Request schema for incoming login payloads."""

    email: EmailStr
    password: str


class AuthMessageResponse(BaseModel):
    """Response schema for success authentication events."""

    message: str
