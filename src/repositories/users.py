from typing import Optional, Sequence

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.repositories.base import BaseRepository
from src.core.security import get_password_hash


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def is_user_exists(self, email: str, username: str) -> bool:
        query = select(User).where(or_(User.email == email, User.username == username))
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def create(self, data: dict) -> User:
        try:
            # Hash password before creating user
            if "password" in data:
                data = data.copy()
                password = data.pop("password")
                # Convert SecretStr to string if needed
                if hasattr(password, "get_secret_value"):
                    password = password.get_secret_value()
                # Truncate password to 72 characters for bcrypt compatibility
                if len(password) > 72:
                    password = password[:72]
                data["password_hash"] = get_password_hash(password)
            
            return await super().create(data)
        except Exception as e:
            raise Exception(f"Failed to create user: {str(e)}")
