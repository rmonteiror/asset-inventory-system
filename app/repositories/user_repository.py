from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        data: UserCreate
    ) -> User:

        hashed_password = hash_password(
            data.password
        )

        user = User(
            full_name=data.full_name,
            email=data.email,
            password_hash=hashed_password,
            role="USER",
            department=data.department,
            position=data.position
        )

        self.session.add(user)

        await self.session.commit()

        await self.session.refresh(user)

        return user

    async def list(
        self
    ) -> list[User]:

        result = await self.session.execute(
            select(User)
        )

        return result.scalars().all()

    async def get(
        self,
        user_id: int
    ) -> User | None:

        result = await self.session.execute(
            select(User).where(
                User.id == user_id
            )
        )

        return result.scalars().first()

    async def get_by_email(
        self,
        email: str
    ) -> User | None:

        result = await self.session.execute(
            select(User).where(
                User.email == email
            )
        )

        return result.scalars().first()

    async def update(
        self,
        user_id: int,
        data: UserUpdate
    ) -> User | None:

        user = await self.get(user_id)

        if not user:
            return None

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "password" in update_data:
            update_data["password_hash"] = hash_password(
                update_data.pop("password")
            )

        for field, value in update_data.items():
            setattr(user, field, value)

        await self.session.commit()

        await self.session.refresh(user)

        return user

    async def delete(
        self,
        user_id: int
    ) -> bool:

        user = await self.get(user_id)

        if not user:
            return False

        await self.session.delete(user)

        await self.session.commit()

        return True