import asyncio 

from fastapi import FastAPI

from db.database import init_models
from api import api


asyncio.get_event_loop().create_task(init_models())

app = FastAPI()

app.include_router(api.router)
