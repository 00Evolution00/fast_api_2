from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.posts import PostCreate, PostResponse, PostUpdate
from src.core.db import database
from src.repositories.posts import PostRepository
from src.core.error_handlers import (
    handle_post_not_found,
    handle_post_creation_error,
    handle_database_error,
)
from src.core.exceptions import PostNotFound, PostCreationError, DatabaseError
from src.services.auth import get_current_active_user, get_db
from src.schemas.users import UserResponse

router = APIRouter()


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user)
):
    try:
        repo = PostRepository(db)
        
        post_data = post.model_dump()
        post_data["author_id"] = current_user.id
        post_data["pub_date"] = post_data["pub_date"]
        
        new_post = await repo.create(post_data)
        return new_post
    except PostCreationError as e:
        raise handle_post_creation_error(e)
    except DatabaseError as e:
        raise handle_database_error(e)


@router.get("/", response_model=List[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)) -> List[PostResponse]:
    try:
        repo = PostRepository(db)
        return await repo.get_all()
    except DatabaseError as e:
        raise handle_database_error(e)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str, 
    db: AsyncSession = Depends(get_db)
):
    try:
        repo = PostRepository(db)
        post = await repo.get_with_validation(post_id)
        return post
    except PostNotFound as e:
        raise handle_post_not_found(e)
    except DatabaseError as e:
        raise handle_database_error(e)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str, 
    post_update: PostUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user)
):
    try:
        repo = PostRepository(db)

        db_post = await repo.get_with_validation(post_id)
        
        # Check if user is the author of the post
        if db_post.author_id != current_user.id:
            raise status.HTTP_403_FORBIDDEN(
                detail="Not authorized to update this post"
            )
        
        update_data = post_update.model_dump(exclude_unset=True)
        updated_post = await repo.update(db_post, update_data)
        return updated_post
    except PostNotFound as e:
        raise handle_post_not_found(e)
    except DatabaseError as e:
        raise handle_database_error(e)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str, 
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user)
):
    try:
        repo = PostRepository(db)

        db_post = await repo.get_with_validation(post_id)
        
        # Check if user is the author of the post
        if db_post.author_id != current_user.id:
            raise status.HTTP_403_FORBIDDEN(
                detail="Not authorized to delete this post"
            )
        
        await repo.delete(db_post)
        return
    except PostNotFound as e:
        raise handle_post_not_found(e)
    except DatabaseError as e:
        raise handle_database_error(e)
