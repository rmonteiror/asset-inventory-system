from fastapi import APIRouter

from app.api import auth
from app.api import users
from app.api import assets

router = APIRouter(
    prefix="/api"
)

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(assets.router)