from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.schemas.base_schema import BaseResponse


class UserResponse(BaseResponse):
    """Response schema for <User> endpoints."""

    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr
    phone_number: str | None = None
    device_token: str | None = None


class UserCreate(BaseModel):
    """Request schema for <User> POST and PUT endpoints."""

    model_config = ConfigDict(str_strip_whitespace=True)

    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr
    phone_number: str | None = None
    device_token: str | None = None
    password: str = Field(..., min_length=6, max_length=16)


class UserUpdate(BaseModel):
    """Request schema for <User> PATCH endpoints."""

    model_config = ConfigDict(str_strip_whitespace=True)

    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    device_token: str | None = None
    password: str | None = Field(default=None, min_length=6, max_length=16)
