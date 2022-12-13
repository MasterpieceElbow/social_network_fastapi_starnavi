import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Table,
)
from sqlalchemy.orm import relationship

from db.database import Base

PostsLikes = Table(
    "post_likes",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column('created', DateTime, default=datetime.datetime.now)
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    last_login = Column(DateTime)
    last_request = Column(DateTime)

    posts = relationship("Post", back_populates="owner")
    liked_posts = relationship("Post", secondary=PostsLikes, back_populates="likes")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True, default="")
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    likes = relationship(
        "User", secondary=PostsLikes, back_populates="liked_posts"
    )
