from typing import Annotated

from fastapi import Cookie, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database.real_database import get_db


class PaginationParams(BaseModel):
    offset: int = Query(default=0, ge=0, description="Number of records to skip")
    limit: int = Query(default=10, ge=1, le=100, description="Max records to return")


DbDependency = Annotated[Session, Depends(get_db)]
PaginationDependency = Annotated[PaginationParams, Depends()]
RefreshTokenDependency = Annotated[str | None, Cookie()]
