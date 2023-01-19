from fastapi import APIRouter

from api.routers import users, posts, analytics, authentication


router = APIRouter(prefix="/api")

router.include_router(users.router)
router.include_router(posts.router)
router.include_router(analytics.router)
router.include_router(authentication.router)
