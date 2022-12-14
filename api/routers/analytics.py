from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    status,
    Query,
    HTTPException,
)
from sqlalchemy.orm import Session

from authentication.dependencies import get_current_user
from db.dependencies import get_db
from db import crud


router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/likes/", response_model=dict[date, int], tags=["likes"])
def likes_by_period(
        db: Session = Depends(get_db),
        date_from: date = Query(),
        date_to: date = Query()
):
    if date_to < date_from:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="date_to should be greater than or equal to date_from"
        )
    return crud.get_likes_within_period_group_by_date(
        date_from=date_from, date_to=date_to, db=db
    )
