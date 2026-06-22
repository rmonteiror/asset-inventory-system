from fastapi import APIRouter
from app.api.endpoints import assets

router = APIRouter(prefix="/api")
router.include_router(assets.router)
