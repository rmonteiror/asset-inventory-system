from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.repositories.maintenance_repository import MaintenanceRepository
from app.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceRead,
    MaintenanceUpdate
)
from app.core.dependencies import get_current_user
from app.core.permissions import require_admin
from app.models.user import User

router = APIRouter(
    prefix="/maintenance",
    tags=["maintenance"]
)


@router.post(
    "/",
    response_model=MaintenanceRead,
    status_code=201
)
async def create_maintenance(
    payload: MaintenanceCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin)
):
    repository = MaintenanceRepository(session)

    try:
        return await repository.create(payload)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=list[MaintenanceRead]
)
async def list_maintenances(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    repository = MaintenanceRepository(session)

    return await repository.list(
        page=page,
        size=size
    )


@router.get(
    "/{maintenance_id}",
    response_model=MaintenanceRead
)
async def get_maintenance(
    maintenance_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    repository = MaintenanceRepository(session)

    maintenance = await repository.get(
        maintenance_id
    )

    if not maintenance:
        raise HTTPException(
            status_code=404,
            detail="Maintenance not found."
        )

    return maintenance


@router.get(
    "/asset/{asset_id}",
    response_model=list[MaintenanceRead]
)
async def list_by_asset(
    asset_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    repository = MaintenanceRepository(session)

    return await repository.list_by_asset(
        asset_id
    )


@router.put(
    "/{maintenance_id}",
    response_model=MaintenanceRead
)
async def update_maintenance(
    maintenance_id: int,
    payload: MaintenanceUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin)
):
    repository = MaintenanceRepository(session)

    try:

        maintenance = await repository.update(
            maintenance_id,
            payload
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    if not maintenance:

        raise HTTPException(
            status_code=404,
            detail="Maintenance not found."
        )

    return maintenance


@router.delete(
    "/{maintenance_id}"
)
async def delete_maintenance(
    maintenance_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin)
):
    repository = MaintenanceRepository(session)

    deleted = await repository.delete(
        maintenance_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Maintenance not found."
        )

    return {
        "message": "Maintenance deleted successfully."
    }