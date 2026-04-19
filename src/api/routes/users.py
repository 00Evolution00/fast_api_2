from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.users import UserResponse, UserUpdate
from src.repositories.users import UserRepository
from src.services.auth import get_current_active_user, get_db
from src.core.exceptions import UserNotFound
from src.core.error_handlers import handle_user_not_found

router = APIRouter()


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(
    current_user: UserResponse = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> List[UserResponse]:
    repo = UserRepository(db)
    return await repo.get_all()


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user)
):
    repo = UserRepository(db)
    user = await repo.get(user_id)
    if user is None:
        raise handle_user_not_found(UserNotFound(user_id))

    # Only allow users to view their own profile (or make it admin-only)
    if user.id != current_user.id and not current_user.is_superuser:
        raise status.HTTP_403_FORBIDDEN(
            detail="Not authorized to view this user"
        )

    return user


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user)
):
    repo = UserRepository(db)

    db_user = await repo.get(user_id)
    if db_user is None:
        raise handle_user_not_found(UserNotFound(user_id))

    # Only allow users to update their own profile (or make it admin-only)
    if db_user.id != current_user.id and not current_user.is_superuser:
        raise status.HTTP_403_FORBIDDEN(
            detail="Not authorized to update this user"
        )

    update_data = user_update.model_dump(exclude_unset=True)
    updated_user = await repo.update(db_user, update_data)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user)
):
    repo = UserRepository(db)

    db_user = await repo.get(user_id)
    if db_user is None:
        raise handle_user_not_found(UserNotFound(user_id))

    # Only allow users to delete their own profile (or make it admin-only)
    if db_user.id != current_user.id and not current_user.is_superuser:
        raise status.HTTP_403_FORBIDDEN(
            detail="Not authorized to delete this user"
        )

    await repo.delete(db_user)
    return
