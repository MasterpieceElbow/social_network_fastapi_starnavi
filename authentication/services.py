from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext

from db import models, crud
from authentication.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def authenticate_user(
        db: Session, username: str, password: str
) -> Optional[models.User]:
    user_db = crud.get_user_by_username(db=db, username=username)
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
