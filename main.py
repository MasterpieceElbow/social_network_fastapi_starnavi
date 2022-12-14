from fastapi import FastAPI

# from routers import users, posts, analytics, authentication
from db.models import Base
from db.database import engine
from api import api


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api.router)

# app.include_router(users.router, prefix="/api")
# app.include_router(posts.router, prefix="/api")
# app.include_router(analytics.router, prefix="/api")
# app.include_router(authentication.router, prefix="/api")
