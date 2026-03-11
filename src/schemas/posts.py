import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(max_length=255)
    text: str
    pub_date: datetime
    is_published: bool = True


class PostCreate(PostBase):
    author_id: uuid.UUID
    category_id: Optional[uuid.UUID] = None
    location_id: Optional[uuid.UUID] = None


class PostUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    is_published: Optional[bool] = None
    category_id: Optional[uuid.UUID] = None
    location_id: Optional[uuid.UUID] = None


class PostResponse(PostBase):
    id: uuid.UUID
    author_id: uuid.UUID
    category_id: Optional[uuid.UUID]
    location_id: Optional[uuid.UUID]
    image: Optional[str] = None
    created_at: datetime
    comment_count: Optional[int] = None
