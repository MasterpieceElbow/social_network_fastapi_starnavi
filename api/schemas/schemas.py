from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    description: Optional[str] = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    last_login: Optional[datetime] = None
    last_request: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserDetail(User):
    posts: list[Post] = []


class UserDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
