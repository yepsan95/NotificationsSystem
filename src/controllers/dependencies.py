from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Cookie, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.security import ALGORITHM, PUBLIC_KEY
from src.database.real_database import get_db
from src.models.user_model import User
from src.repositories.user_repository import UserRepository


class PaginationParams(BaseModel):
    offset: int = Query(default=0, ge=0, description="Number of records to skip")
    limit: int = Query(default=10, ge=1, le=100, description="Max records to return")


DbDependency = Annotated[Session, Depends(get_db)]
PaginationDependency = Annotated[PaginationParams, Depends()]
RefreshTokenDependency = Annotated[str | None, Cookie(alias="refresh_token")]


def get_current_user(request: Request, db: DbDependency) -> User:
    """Dependency protector to extract, decode and validate the access token from cookies."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise credentials_exception
    try:
        payload = jwt.decode(access_token, PUBLIC_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = UUID(user_id_str)
    except (jwt.PyJWTError, ValueError):
        raise credentials_exception
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user


CurrentUserDependency = Annotated[User, Depends(get_current_user)]
