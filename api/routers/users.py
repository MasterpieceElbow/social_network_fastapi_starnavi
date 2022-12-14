from fastapi import APIRouter, Depends, HTTPException, status

from db.dependencies import get_db
from sqlalchemy.orm import Session

from db import crud
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
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db=db)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise missing_user_exception

    return db_user


@router.get(
    "/{user_id}/posts/",
    response_model=list[schemas.Post],
    tags=["posts"],
)
def read_user_posts(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise missing_user_exception

    return db_user.posts


@router.get(
    "/{user_id}/likes/",
    response_model=list[schemas.Post],
    tags=["likes"],
)
def read_user_liked_posts(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise missing_user_exception

    return db_user.liked_posts
