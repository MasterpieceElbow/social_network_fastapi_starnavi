from fastapi import FastAPI

from db.models import Base
from db.database import engine
from api import api


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api.router)
