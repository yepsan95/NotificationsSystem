from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    """Base response class for HTTP requests responses."""
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
