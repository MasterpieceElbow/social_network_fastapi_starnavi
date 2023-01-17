from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from db import crud
from db.dependencies import get_db
from api.schemas import schemas
from authentication.dependencies import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
)

missing_user_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist"
)


@router.get("/", response_model=list[schemas.User])
async def read_users(db: AsyncSession = Depends(get_db)):
    await db.commit()
    return await crud.get_users(db=db)


@router.get("/{user_id}", response_model=schemas.UserDetail)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    await db.commit()
    db_user = await crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise missing_user_exception

    return db_user


@router.get(
    "/{user_id}/posts/",
    response_model=list[schemas.Post],
    tags=["posts"],
)
async def read_user_posts(user_id: int, db: AsyncSession = Depends(get_db)):
    await db.commit()
    return await crud.get_user_posts(db=db, user_id=user_id)


@router.get(
    "/{user_id}/likes/",
    response_model=list[schemas.Post],
    tags=["likes"],
)
async def read_user_liked_posts(user_id: int, db: AsyncSession = Depends(get_db)):
    await db.commit()
    return await crud.get_user_liked_posts(db=db, user_id=user_id)
