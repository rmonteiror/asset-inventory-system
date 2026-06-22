from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate


class AssetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: AssetCreate) -> Asset:
        asset = Asset(**data.model_dump())

        self.session.add(asset)

        await self.session.commit()

        await self.session.refresh(asset)

        return asset

    async def list(self) -> list[Asset]:
        result = await self.session.execute(
            select(Asset)
        )

        return result.scalars().all()

    async def get(self, asset_id: int) -> Asset | None:
        result = await self.session.execute(
            select(Asset).where(
                Asset.id == asset_id
            )
        )

        return result.scalars().first()

    async def update(
        self,
        asset_id: int,
        data: AssetUpdate
    ) -> Asset | None:

        asset = await self.get(asset_id)

        if not asset:
            return None

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(asset, field, value)

        await self.session.commit()

        await self.session.refresh(asset)

        return asset

    async def delete(
        self,
        asset_id: int
    ) -> bool:

        asset = await self.get(asset_id)

        if not asset:
            return False

        await self.session.delete(asset)

        await self.session.commit()

        return True