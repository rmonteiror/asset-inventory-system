from fastapi import Depends, HTTPException

from app.core.dependencies import get_current_user
from app.models.user import User


async def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:

    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action."
        )

    return current_user