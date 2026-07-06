from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.license import License
from app.schemas.license import (
    LicenseCreate,
    LicenseUpdate
)


class LicenseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        data: LicenseCreate
    ) -> License:

        license = License(
            **data.model_dump()
        )

        self.session.add(license)

        await self.session.commit()

        await self.session.refresh(license)

        return license

    async def list(
        self
    ) -> list[License]:

        result = await self.session.execute(
            select(License)
        )

        return result.scalars().all()

    async def get(
        self,
        license_id: int
    ) -> License | None:

        result = await self.session.execute(
            select(License).where(
                License.id == license_id
            )
        )

        return result.scalars().first()

    async def update(
        self,
        license_id: int,
        data: LicenseUpdate
    ) -> License | None:

        license = await self.get(
            license_id
        )

        if not license:
            return None

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                license,
                field,
                value
            )

        await self.session.commit()

        await self.session.refresh(
            license
        )

        return license

    async def delete(
        self,
        license_id: int
    ) -> bool:

        license = await self.get(
            license_id
        )

        if not license:
            return False

        await self.session.delete(
            license
        )

        await self.session.commit()

        return True