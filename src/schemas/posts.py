from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.core.validators import PostValidators


class PostBase(BaseModel):
    title: str = Field(max_length=255)
    text: str
    pub_date: datetime
    is_published: bool = True


class PostCreate(PostBase, PostValidators):
    author_id: str
    category_id: Optional[str] = None
    location_id: Optional[str] = None


class PostUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    is_published: Optional[bool] = None
    category_id: Optional[str] = None
    location_id: Optional[str] = None


class PostResponse(PostBase):
    id: str
    author_id: str
    category_id: Optional[str]
    location_id: Optional[str]
    image: Optional[str] = None
    created_at: datetime
    comment_count: Optional[int] = None
