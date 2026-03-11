import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LocationBase(BaseModel):
    name: str = Field(max_length=255)
    is_published: bool = True


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    is_published: Optional[bool] = None


class Location(LocationBase):
    id: uuid.UUID
    created_at: datetime
