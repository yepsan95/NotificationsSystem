from fastapi import Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    offset: int = Query(default=0, ge=0, description="Number of records to skip")
    limit: int = Query(default=10, ge=1, le=100, description="Max records to return")
