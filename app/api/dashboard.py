from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.repositories.dashboard_repository import DashboardRepository
from app.schemas.dashboard import DashboardSummary
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"]
)


@router.get(
    "/summary",
    response_model=DashboardSummary
)
async def dashboard_summary(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    repository = DashboardRepository(session)

    return await repository.get_summary()