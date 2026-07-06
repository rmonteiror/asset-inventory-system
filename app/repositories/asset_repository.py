from sqlalchemy import select, or_
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

    async def list(
        self,
        search: str | None = None,
        status: str | None = None,
        asset_type: str | None = None,
        location: str | None = None,
        page: int = 1,
        size: int = 10
    ) -> list[Asset]:

        query = select(Asset)

        if search:
            query = query.where(
                or_(
                    Asset.name.ilike(f"%{search}%"),
                    Asset.asset_tag.ilike(f"%{search}%"),
                    Asset.serial_number.ilike(f"%{search}%")
                )
            )

        if status:
            query = query.where(
                Asset.status == status
            )

        if asset_type:
            query = query.where(
                Asset.asset_type == asset_type
            )

        if location:
            query = query.where(
                Asset.location.ilike(f"%{location}%")
            )

        offset = (page - 1) * size

        query = query.offset(offset).limit(size)

        result = await self.session.execute(query)

        return result.scalars().all()

    async def get(
        self,
        asset_id: int
    ) -> Asset | None:

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

    async def assign_user(
        self,
        asset_id: int,
        user_id: int
    ) -> Asset | None:

        asset = await self.get(asset_id)

        if not asset:
            return None

        asset.assigned_user_id = user_id

        await self.session.commit()

        await self.session.refresh(asset)

        return asset

    async def unassign_user(
        self,
        asset_id: int
    ) -> Asset | None:

        asset = await self.get(asset_id)

        if not asset:
            return None

        asset.assigned_user_id = None

        await self.session.commit()

        await self.session.refresh(asset)

        return asset