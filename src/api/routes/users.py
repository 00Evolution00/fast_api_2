import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.users import UserCreate, UserResponse, UserUpdate
from src.core.db import database
from src.repositories.users import UserRepository

router = APIRouter()


async def get_db():
    async with database.session() as session:
        yield session


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)

    if await repo.is_user_exists(email=user_in.email, username=user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists",
        )

    user_data = user_in.model_dump()
    password_plain = user_in.password.get_secret_value()
    user_data["password_hash"] = password_plain
    del user_data["password"]

    new_user = await repo.create(user_data)
    return new_user


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_db)) -> List[UserResponse]:
    repo = UserRepository(db)
    return await repo.get_all()


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: uuid.UUID, user_update: UserUpdate, db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)

    db_user = await repo.get(user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    update_data = user_update.model_dump(exclude_unset=True)
    updated_user = await repo.update(db_user, update_data)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)

    db_user = await repo.get(user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    await repo.delete(db_user)
    return
