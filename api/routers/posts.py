from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
)
from sqlalchemy.orm import Session

from db.dependencies import get_db
from db import crud
from api.schemas import schemas
from authentication.dependencies import get_current_user


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db=db)


@router.post("/", response_model=schemas.Post)
def create_post(
        post: schemas.PostCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    return crud.create_user_post(db=db, post=post, user_id=current_user.id)


@router.get("/{post_id}/", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    return crud.get_post(db=db, post_id=post_id)


@router.get(
    "/{post_id}/likes/", response_model=list[schemas.User], tags=["likes"]
)
def read_post_likes(post_id: int, db: Session = Depends(get_db)):
    return crud.get_post_likes(post_id=post_id, db=db)


@router.post("/{post_id}/like/", tags=["likes"])
def like_post(
        post_id: int,
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    is_liked = crud.get_user_liked_post(
        post_id=post_id, user_id=current_user.id, db=db
    )

    if is_liked:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Post is already liked by this user")

    crud.like_post(db=db, post_id=post_id, user_id=current_user.id)
    return {"detail": f"User {current_user.id} liked post {post_id}"}


@router.delete("/{post_id}/unlike/", tags=["likes"])
def unlike_post(
        post_id: int,
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    is_liked = crud.get_user_liked_post(
        post_id=post_id, user_id=current_user.id, db=db
    )

    if not is_liked:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Post was not liked by this user")

    crud.unlike_post(db=db, post_id=post_id, user_id=current_user.id)
    return {"detail": f"User {current_user.id} unliked post {post_id}"}
