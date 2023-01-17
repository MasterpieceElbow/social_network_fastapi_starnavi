from datetime import date, datetime, timedelta

from sqlalchemy.orm import selectinload
from sqlalchemy import func, select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db import models
from api.schemas import schemas


# User
async def get_user(db: AsyncSession, user_id: int) -> models.User:
    users = await db.execute(select(models.User).filter_by(id=user_id).options(selectinload(models.User.posts)))
    return users.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> models.User:
    users = await db.execute(select(models.User).filter_by(username=username).options(selectinload(models.User.posts)))
    return users.scalars().first()


async def get_users(db: AsyncSession) -> list[models.User]:
    users = await db.execute(select(models.User))
    return users.scalars().all()


async def update_user_last_login(user_id: int, db: AsyncSession):
    await db.execute(update(models.User).where(models.User.id == user_id).values(last_login = datetime.now()))


async def update_user_last_request(user_id: int, db: AsyncSession):
    await db.execute(update(models.User).where(models.User.id == user_id).values(last_request = datetime.now()))


# Posts
async def get_posts(db: AsyncSession) -> list[models.Post]:
    posts = await db.execute(select(models.Post))
    return posts.scalars().all()


async def get_post(db: AsyncSession, post_id: int) -> models.Post:
    posts = await db.execute(select(models.Post).filter_by(id=post_id))
    return posts.scalars().first()


async def get_user_posts(db: AsyncSession, user_id: int) -> list[models.Post]:
    posts = await db.execute(select(models.Post).filter(models.Post.owner_id==user_id))
    return posts.scalars().all()


async def get_post_likes(db: AsyncSession, post_id: int) -> list[models.User]:
    posts = await db.execute(
        select(models.Post).filter_by(id=post_id).options(selectinload(models.Post.likes))
    )
    post = posts.scalars().first()
    if post is None:
        return 
    return post.likes


def create_user_post(
        db: AsyncSession,
        post: schemas.PostCreate,
        user_id: int
) -> models.Post:
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    return db_post


# Likes
async def like_post(db: AsyncSession, post_id: int, user_id: int) -> None:
    await db.execute(
        insert(models.PostsLikes).values(post_id=post_id, user_id=user_id)
    )


async def unlike_post(db: AsyncSession, post_id: int, user_id: int) -> None:
    deleted = await db.execute(
        delete(models.PostsLikes).where(
            models.PostsLikes.c.post_id == post_id, 
            models.PostsLikes.c.user_id == user_id,
        ).returning(models.PostsLikes.c.id)
    )
    return deleted.fetchall()


async def get_user_liked_posts(
        db: AsyncSession, 
        user_id: int,
) -> list[models.Post]:
    posts = await db.execute(
        select(models.Post).join(models.User, models.Post.likes).filter(models.User.id == user_id)
    )
    return posts.scalars().all()


async def get_likes_within_period_group_by_date(
        db: AsyncSession, date_from: date, date_to: date
) -> dict[str, int]:
    likes = await db.execute(
        select(
            func.date(models.PostsLikes.columns.created),
            func.count(models.PostsLikes.columns.id),
        ).filter(
            models.PostsLikes.columns.created.between(
                date_from, date_to + timedelta(days=1)
            )
        ).group_by(
            func.date(models.PostsLikes.columns.created)
        )
    )
    data = {_date: likes for _date, likes in likes.all()}
    print(data)
    return data
