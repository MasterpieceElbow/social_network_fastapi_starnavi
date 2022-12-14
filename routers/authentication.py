from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.dependencies import get_db
from db import crud, schemas
from authentication.services import (
    authenticate_user,
    create_access_token,
    create_user,
)


router = APIRouter(
    tags=["authentication"],
)


@router.post("/token/", response_model=schemas.Token)
def login_for_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    crud.update_user_last_login(user=user, db=db)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/sign-up/", response_model=schemas.User)
def sign_up_user(form_data: OAuth2PasswordRequestForm = Depends(),
                 db: Session = Depends(get_db)):
    user = schemas.UserCreate(
        username=form_data.username, password=form_data.password
    )
    db_user = create_user(db=db, user=user)
    return db_user
