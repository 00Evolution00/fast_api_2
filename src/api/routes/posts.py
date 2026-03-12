from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.posts import PostCreate, PostResponse, PostUpdate
from src.core.db import database
from src.repositories.posts import PostRepository

router = APIRouter()


async def get_db():
    async with database.session() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    repo = PostRepository(db)
    
    post_data = post.model_dump()
    post_data["pub_date"] = post_data["pub_date"]
    
    new_post = await repo.create(post_data)
    return new_post


@router.get("/", response_model=List[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)) -> List[PostResponse]:
    repo = PostRepository(db)
    return await repo.get_all()


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: str, db: AsyncSession = Depends(get_db)):
    repo = PostRepository(db)
    post = await repo.get(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str, post_update: PostUpdate, db: AsyncSession = Depends(get_db)
):
    repo = PostRepository(db)

    db_post = await repo.get(post_id)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    update_data = post_update.model_dump(exclude_unset=True)
    updated_post = await repo.update(db_post, update_data)
    return updated_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: str, db: AsyncSession = Depends(get_db)):
    repo = PostRepository(db)

    db_post = await repo.get(post_id)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    await repo.delete(db_post)
    return
