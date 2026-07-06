from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate
)
from app.core.dependencies import get_current_user
from app.core.permissions import require_admin
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    "/",
    response_model=UserRead,
    status_code=201
)
async def create_user(
    payload: UserCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin)
):
    user_repo = UserRepository(session)

    user = await user_repo.create(payload)

    return user


@router.get(
    "/",
    response_model=list[UserRead]
)
async def list_users(
    session: AsyncSession = Depends(get_session)
):
    user_repo = UserRepository(session)

    return await user_repo.list()


@router.get(
    "/me",
    response_model=UserRead
)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserRead
)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    user_repo = UserRepository(session)

    user = await user_repo.get(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserRead
)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    session: AsyncSession = Depends(get_session)
):
    user_repo = UserRepository(session)

    user = await user_repo.update(
        user_id,
        payload
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.delete(
    "/{user_id}"
)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_admin)
):
    user_repo = UserRepository(session)

    deleted = await user_repo.delete(
        user_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }