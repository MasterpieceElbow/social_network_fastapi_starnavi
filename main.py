import asyncio 

from fastapi import FastAPI

from db.database import init_models
from api import api


asyncio.get_event_loop().create_task(init_models())
# asyncio.run(init_models())
# Base.metadata.create_all(bind=async_engine)


app = FastAPI()

app.include_router(api.router)
