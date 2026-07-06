from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.repositories.asset_repository import AssetRepository
from app.schemas.asset import (
    AssetCreate,
    AssetRead,
    AssetUpdate
)
from app.core.dependencies import get_current_user
from app.core.permissions import require_admin
from app.models.user import User

router = APIRouter(
    prefix="/assets",
    tags=["assets"]
)


@router.post(
    "/",
    response_model=AssetRead,
    status_code=201
)
async def create_asset(
    payload: AssetCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin)
):
    asset_repo = AssetRepository(session)

    return await asset_repo.create(payload)


@router.get(
    "/",
    response_model=list[AssetRead]
)
async def list_assets(
    search: str | None = Query(default=None),
    status: str | None = Query(default=None),
    asset_type: str | None = Query(default=None),
    location: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    asset_repo = AssetRepository(session)

    return await asset_repo.list(
        search=search,
        status=status,
        asset_type=asset_type,
        location=location,
        page=page,
        size=size
    )


@router.get(
    "/{asset_id}",
    response_model=AssetRead
)
async def get_asset(
    asset_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    asset_repo = AssetRepository(session)

    asset = await asset_repo.get(asset_id)

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset


@router.put(
    "/{asset_id}",
    response_model=AssetRead
)
async def update_asset(
    asset_id: int,
    payload: AssetUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin)
):
    asset_repo = AssetRepository(session)

    asset = await asset_repo.update(
        asset_id,
        payload
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset


@router.put(
    "/{asset_id}/assign/{user_id}",
    response_model=AssetRead
)
async def assign_asset(
    asset_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin)
):
    asset_repo = AssetRepository(session)

    asset = await asset_repo.assign_user(
        asset_id,
        user_id
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset


@router.delete(
    "/{asset_id}/unassign",
    response_model=AssetRead
)
async def unassign_asset(
    asset_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin)
):
    asset_repo = AssetRepository(session)

    asset = await asset_repo.unassign_user(
        asset_id
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset


@router.delete(
    "/{asset_id}"
)
async def delete_asset(
    asset_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin)
):
    asset_repo = AssetRepository(session)

    deleted = await asset_repo.delete(asset_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return {
        "message": "Asset deleted successfully"
    }