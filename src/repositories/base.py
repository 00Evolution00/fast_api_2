from typing import Any, Generic, Optional, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, obj_id: Any) -> Optional[T]:
        return await self.session.get(self.model, obj_id)

    async def get_all(self) -> Sequence[T]:
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, data: dict) -> T:
        db_obj = self.model(**data)
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def update(self, db_obj: T, update_data: dict) -> T:
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def delete(self, db_obj: T) -> None:
        await self.session.delete(db_obj)
        await self.session.flush()
