from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from db.dependencies import get_db
from db import crud
from api.schemas import schemas
from authentication.dependencies import get_current_user


missing_post_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Post doesn't exist"
)


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=list[schemas.Post])
async def read_posts(db: AsyncSession = Depends(get_db)):
    await db.commit()
    return await crud.get_posts(db=db)


@router.post("/", response_model=schemas.Post) 
async def create_post(
        response: Response,
        post: schemas.PostCreate,
        db: AsyncSession = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    response.status_code = status.HTTP_201_CREATED
    post = crud.create_user_post(db=db, post=post, user_id=current_user.id)
    await db.commit()
    return post


@router.get("/{post_id}/", response_model=schemas.Post)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db)):
    await db.commit()
    post = await crud.get_post(db=db, post_id=post_id)
    if post is None:
        raise missing_post_exception
    return post


@router.get(
    "/{post_id}/likes/", response_model=list[schemas.User], tags=["likes"]
)
async def read_post_likes(post_id: int, db: AsyncSession = Depends(get_db)):
    await db.commit()
    likes = await crud.get_post_likes(post_id=post_id, db=db)
    if likes is None:
        raise missing_post_exception
    return likes


@router.post("/{post_id}/like/", tags=["likes"])
async def like_post(
        post_id: int,
        response: Response,
        current_user: schemas.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    try:
        await crud.like_post(db=db, post_id=post_id, user_id=current_user.id)
    except IntegrityError:
        await db.rollback()
        response.status_code = status.HTTP_200_OK
        return {"detail": "Post is already liked by this user"}

    await db.commit()
    response.status_code = status.HTTP_201_CREATED
    return {"detail": f"User {current_user.id} liked post {post_id}"}


@router.delete("/{post_id}/unlike/", tags=["likes"])
async def unlike_post(
        post_id: int,
        response: Response,
        current_user: schemas.User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):

    unliked = await crud.unlike_post(db=db, post_id=post_id, user_id=current_user.id)
    await db.commit()
    
    if len(unliked) == 0:
        response.status_code = status.HTTP_200_OK
        return {"detail": "Post was not liked by this user"}
    
    response.status_code = status.HTTP_201_CREATED
    return {"detail": f"User {current_user.id} unliked post {post_id}"}
