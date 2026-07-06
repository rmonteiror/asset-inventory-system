from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.repositories.license_repository import LicenseRepository
from app.schemas.license import (
    LicenseCreate,
    LicenseRead,
    LicenseUpdate
)

router = APIRouter(
    prefix="/licenses",
    tags=["licenses"]
)


@router.post(
    "/",
    response_model=LicenseRead,
    status_code=201
)
async def create_license(
    payload: LicenseCreate,
    session: AsyncSession = Depends(get_session)
):
    license_repo = LicenseRepository(session)

    license = await license_repo.create(payload)

    return license


@router.get(
    "/",
    response_model=list[LicenseRead]
)
async def list_licenses(
    session: AsyncSession = Depends(get_session)
):
    license_repo = LicenseRepository(session)

    return await license_repo.list()


@router.get(
    "/{license_id}",
    response_model=LicenseRead
)
async def get_license(
    license_id: int,
    session: AsyncSession = Depends(get_session)
):
    license_repo = LicenseRepository(session)

    license = await license_repo.get(
        license_id
    )

    if not license:
        raise HTTPException(
            status_code=404,
            detail="License not found"
        )

    return license


@router.put(
    "/{license_id}",
    response_model=LicenseRead
)
async def update_license(
    license_id: int,
    payload: LicenseUpdate,
    session: AsyncSession = Depends(get_session)
):
    license_repo = LicenseRepository(session)

    license = await license_repo.update(
        license_id,
        payload
    )

    if not license:
        raise HTTPException(
            status_code=404,
            detail="License not found"
        )

    return license


@router.delete(
    "/{license_id}"
)
async def delete_license(
    license_id: int,
    session: AsyncSession = Depends(get_session)
):
    license_repo = LicenseRepository(session)

    deleted = await license_repo.delete(
        license_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="License not found"
        )

    return {
        "message": "License deleted successfully"
    }