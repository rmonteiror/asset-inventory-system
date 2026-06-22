from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.asset_repository import AssetRepository
from app.schemas.asset import (
    AssetCreate,
    AssetRead,
    AssetUpdate
)
from app.database import get_session

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
    session: AsyncSession = Depends(get_session)
):
    asset_repo = AssetRepository(session)

    asset = await asset_repo.create(payload)

    return asset


@router.get(
    "/",
    response_model=list[AssetRead]
)
async def list_assets(
    session: AsyncSession = Depends(get_session)
):
    asset_repo = AssetRepository(session)

    return await asset_repo.list()


@router.get(
    "/{asset_id}",
    response_model=AssetRead
)
async def get_asset(
    asset_id: int,
    session: AsyncSession = Depends(get_session)
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
    session: AsyncSession = Depends(get_session)
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


@router.delete(
    "/{asset_id}"
)
async def delete_asset(
    asset_id: int,
    session: AsyncSession = Depends(get_session)
):
    asset_repo = AssetRepository(session)

    deleted = await asset_repo.delete(
        asset_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return {
        "message": "Asset deleted successfully"
    }