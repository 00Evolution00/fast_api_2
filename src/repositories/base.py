from typing import Any, Generic, Optional, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import Base
from src.core.exceptions import DatabaseError

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, obj_id: Any) -> Optional[T]:
        try:
            return await self.session.get(self.model, obj_id)
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))

    async def get_all(self) -> Sequence[T]:
        try:
            query = select(self.model)
            result = await self.session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))

    async def create(self, data: dict) -> T:
        try:
            db_obj = self.model(**data)
            self.session.add(db_obj)
            await self.session.flush()
            await self.session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))

    async def update(self, db_obj: T, update_data: dict) -> T:
        try:
            for field in update_data:
                if hasattr(db_obj, field):
                    setattr(db_obj, field, update_data[field])

            self.session.add(db_obj)
            await self.session.flush()
            return db_obj
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))

    async def delete(self, db_obj: T) -> None:
        try:
            await self.session.delete(db_obj)
            await self.session.flush()
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))
