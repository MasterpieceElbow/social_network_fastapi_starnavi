from fastapi import APIRouter

from api.routers import users, posts, analytics, authentication
from db.models import Base
from db.database import async_engine


# Base.metadata.create_all(bind=async_engine)

router = APIRouter(prefix="/api")


router.include_router(users.router)
router.include_router(posts.router)
router.include_router(analytics.router)
router.include_router(authentication.router)
