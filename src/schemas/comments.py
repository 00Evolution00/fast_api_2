import uuid
from datetime import datetime

from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: uuid.UUID
    post_id: uuid.UUID
    author_id: uuid.UUID
    created_at: datetime
