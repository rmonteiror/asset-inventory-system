from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.asset import Asset
from app.schemas.asset import AssetCreate

class AssetRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: AssetCreate) -> Asset:
        asset = Asset(**data.dict())
        self.session.add(asset)
        await self.session.commit()
        await self.session.refresh(asset)
        return asset

    async def list(self) -> list[Asset]:
        result = await self.session.execute(select(Asset))
        return result.scalars().all()

    async def get(self, asset_id: int) -> Asset | None:
        result = await self.session.execute(select(Asset).where(Asset.id == asset_id))
        return result.scalars().first()
