from fastapi import APIRouter

from app.api import auth
from app.api import users
from app.api import assets
from app.api import licenses
from app.api import dashboard
from app.api import maintenance

router = APIRouter(
    prefix="/api"
)

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(assets.router)
router.include_router(licenses.router)
router.include_router(dashboard.router)
router.include_router(maintenance.router)