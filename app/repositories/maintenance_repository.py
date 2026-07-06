from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.maintenance import Maintenance
from app.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceUpdate
)


class MaintenanceRepository:

    def __init__(
        self,
        session: AsyncSession
    ):
        self.session = session

    async def create(
        self,
        data: MaintenanceCreate
    ) -> Maintenance:

        asset = await self.session.get(
            Asset,
            data.asset_id
        )

        if not asset:
            raise ValueError(
                "Asset not found."
            )

        maintenance = Maintenance(
            **data.model_dump()
        )

        self.session.add(maintenance)

        await self.session.commit()

        await self.session.refresh(
            maintenance
        )

        return maintenance

    async def get_all(
        self,
        page: int = 1,
        size: int = 10
    ) -> list[Maintenance]:

        offset = (page - 1) * size

        result = await self.session.execute(
            select(Maintenance)
            .offset(offset)
            .limit(size)
        )

        return result.scalars().all()

    async def get(
        self,
        maintenance_id: int
    ) -> Maintenance | None:

        result = await self.session.execute(
            select(Maintenance).where(
                Maintenance.id == maintenance_id
            )
        )

        return result.scalars().first()

    async def update(
        self,
        maintenance_id: int,
        data: MaintenanceUpdate
    ) -> Maintenance | None:

        maintenance = await self.get(
            maintenance_id
        )

        if not maintenance:
            return None

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "asset_id" in update_data:

            asset = await self.session.get(
                Asset,
                update_data["asset_id"]
            )

            if not asset:
                raise ValueError(
                    "Asset not found."
                )

        for field, value in update_data.items():

            setattr(
                maintenance,
                field,
                value
            )

        await self.session.commit()

        await self.session.refresh(
            maintenance
        )

        return maintenance

    async def delete(
        self,
        maintenance_id: int
    ) -> bool:

        maintenance = await self.get(
            maintenance_id
        )

        if not maintenance:
            return False

        await self.session.delete(
            maintenance
        )

        await self.session.commit()

        return True

    async def get_by_asset(
        self,
        asset_id: int
    ) -> list[Maintenance]:

        result = await self.session.execute(
            select(Maintenance).where(
                Maintenance.asset_id == asset_id
            )
        )

        return result.scalars().all()