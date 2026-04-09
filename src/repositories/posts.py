from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.posts import Post
from src.repositories.base import BaseRepository
from src.core.exceptions import PostNotFound, PostCreationError


class PostRepository(BaseRepository[Post]):
    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)

    async def get_by_author(self, author_id: str) -> Sequence[Post]:
        try:
            query = select(Post).where(Post.author_id == author_id)
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            raise PostCreationError(f"Failed to get posts by author: {str(e)}")

    async def get_published(self) -> Sequence[Post]:
        try:
            query = select(Post).where(Post.is_published)
            result = await self.session.execute(query)
            return result.scalars().all()
        except Exception as e:
            raise PostCreationError(f"Failed to get published posts: {str(e)}")

    async def get_with_validation(self, post_id: str) -> Post:
        post = await self.get(post_id)
        if post is None:
            raise PostNotFound(post_id)
        return post
