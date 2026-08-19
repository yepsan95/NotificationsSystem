from pydantic import BaseModel, Field, EmailStr, ConfigDict
from src.schemas.base_schema import BaseResponse


class UserResponse(BaseResponse):
    """Response model for <User> GET endpoints."""
    
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr


class UserCreate(BaseModel):
    """Request model for <User> POST endpoints."""

    model_config = ConfigDict(str_strip_whitespace=True)

    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=16)


class UserUpdate(BaseModel):
    """Request model for <User> PATCH endpoints."""

    model_config = ConfigDict(str_strip_whitespace=True)

    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr
