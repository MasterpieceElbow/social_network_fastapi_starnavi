from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    Response,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.dependencies import get_db
from db import crud
from api.schemas import schemas
from authentication.services import (
    authenticate_user,
    create_access_token,
    create_user,
)


router = APIRouter(
    tags=["authentication"],
)


@router.post("/token/", response_model=schemas.Token)
def login(
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
def sign_up_user(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user_db = crud.get_user_by_username(db=db, username=form_data.username)
    if user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with provided username already exists",
        )

    user = schemas.UserCreate(
        username=form_data.username, password=form_data.password
    )
    db_user = create_user(db=db, user=user)
    response.status_code = status.HTTP_201_CREATED
    return db_user
