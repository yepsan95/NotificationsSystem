from pydantic import BaseModel, EmailStr
from src.schemas.base_schema import BaseResponse


class UserResponse(BaseResponse):
    """Response model for <User> GET endpoints."""
    
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr


class UserCreate(BaseModel):
    """Request model for <User> POST endpoints."""
    
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Request model for <User> PATCH endpoints."""

    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr
