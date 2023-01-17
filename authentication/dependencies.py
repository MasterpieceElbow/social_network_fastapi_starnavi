from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from db import models, crud
from db.dependencies import get_db
from api.schemas import schemas
from authentication.config import (
    SECRET_KEY,
    ALGORITHM,
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token/")


async def get_current_user(
        db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await crud.get_user_by_username(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    await crud.update_user_last_request(user_id=user.id, db=db)
    db.commit()
    return user
