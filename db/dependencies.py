from db.database import SessionLocal
from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

from db import models, crud, schemas


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
