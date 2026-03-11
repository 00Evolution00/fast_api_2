import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    title: str = Field(max_length=255)
    description: str
    slug: str
    is_published: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    slug: Optional[str] = None
    is_published: Optional[bool] = None


class CategoryResponse(CategoryBase):
    id: uuid.UUID
    created_at: datetime
