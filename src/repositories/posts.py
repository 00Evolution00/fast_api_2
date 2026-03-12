from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.posts import Post
from src.repositories.base import BaseRepository


class PostRepository(BaseRepository[Post]):
    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)

    async def get_by_author(self, author_id: str) -> Sequence[Post]:
        query = select(Post).where(Post.author_id == author_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_published(self) -> Sequence[Post]:
        query = select(Post).where(Post.is_published)
        result = await self.session.execute(query)
        return result.scalars().all()
