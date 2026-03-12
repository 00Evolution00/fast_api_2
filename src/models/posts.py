import uuid
from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(
        String(), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(255))
    text: Mapped[str]
    pub_date: Mapped[datetime]
    is_published: Mapped[bool] = mapped_column(default=True)
    author_id: Mapped[str] = mapped_column(String())
    category_id: Mapped[str] = mapped_column(String(), nullable=True)
    location_id: Mapped[str] = mapped_column(String(), nullable=True)
    image: Mapped[str] = mapped_column(String(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    comment_count: Mapped[int] = mapped_column(nullable=True)
