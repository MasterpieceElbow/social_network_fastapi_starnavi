from datetime import date, datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import func
from jose import jwt
from passlib.context import CryptContext

from db import models, schemas


# JWT
SECRET_KEY = "2516a1198860b4112a0df38409991c3d8c3a48e6c920493fc3ca9394ec722fd6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def authenticate_user(
        db: Session, username: str, password: str
) -> Optional[models.User]:
    user_db = get_user_by_username(db=db, username=username)
    if not user_db:
        return
    if not verify_password(password, user_db.hashed_password):
        return
    return user_db


def create_access_token(
        data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# User
def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session) -> list[models.User]:
    return db.query(models.User).all()


def update_user_last_login(user: models.User, db: Session):
    user.last_login = datetime.now()
    db.commit()


def update_user_last_request(user: models.User, db: Session):
    user.last_request = datetime.now()
    db.commit()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Posts
def get_posts(db: Session) -> list[models.Post]:
    return db.query(models.Post).all()


def get_post(db: Session, post_id: int) -> models.Post:
    return db.query(models.Post).filter_by(id=post_id).first()


def get_post_likes(db: Session, post_id: int) -> list[models.User]:
    return db.query(models.Post).filter_by(id=post_id).first().likes


def create_user_post(
        db: Session,
        post: schemas.PostCreate,
        user_id: int
) -> models.Post:
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


# Likes
def like_post(db: Session, post_id: int, user_id: int) -> None:
    user = db.query(models.User).filter_by(id=user_id).first()
    post = db.query(models.Post).filter_by(id=post_id).first()
    post.likes.append(user)
    db.commit()


def unlike_post(db: Session, post_id: int, user_id: int) -> None:
    user = db.query(models.User).filter_by(id=user_id).first()
    post = db.query(models.Post).filter_by(id=post_id).first()
    post.likes.remove(user)
    db.commit()


def user_liked_post(
        db: Session,
        post_id: int,
        user_id: int,
):
    liked = db.query(models.PostsLikes).filter_by(
        post_id=post_id, user_id=user_id
    ).first()
    return liked


def get_likes_within_period_group_by_date(
        db: Session, date_from: date, date_to: date
) -> dict[str, int]:
    likes = db.query(
        func.strftime("%Y-%m-%d", models.PostsLikes.columns.created),
        func.count(models.PostsLikes.columns.id),
    ).filter(
        models.PostsLikes.columns.created.between(
            date_from, date_to + timedelta(days=1)
        )
    ).group_by(
        func.strftime("%Y-%m-%d", models.PostsLikes.columns.created)
    ).all()
    return {_date: likes for _date, likes in likes}
