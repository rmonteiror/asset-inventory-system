from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.license import License
from app.models.user import User


class DashboardRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_summary(self):

        total_users = await self.session.scalar(
            select(func.count(User.id))
        )

        total_assets = await self.session.scalar(
            select(func.count(Asset.id))
        )

        total_licenses = await self.session.scalar(
            select(func.count(License.id))
        )

        available_assets = await self.session.scalar(
            select(func.count(Asset.id)).where(
                Asset.status == "AVAILABLE"
            )
        )

        assigned_assets = await self.session.scalar(
            select(func.count(Asset.id)).where(
                Asset.assigned_user_id.is_not(None)
            )
        )

        maintenance_assets = await self.session.scalar(
            select(func.count(Asset.id)).where(
                Asset.status == "MAINTENANCE"
            )
        )

        retired_assets = await self.session.scalar(
            select(func.count(Asset.id)).where(
                Asset.status == "RETIRED"
            )
        )

        expired_licenses = await self.session.scalar(
            select(func.count(License.id)).where(
                License.status == "EXPIRED"
            )
        )

        return {
            "users": total_users,
            "assets": total_assets,
            "licenses": total_licenses,
            "available_assets": available_assets,
            "assigned_assets": assigned_assets,
            "maintenance_assets": maintenance_assets,
            "retired_assets": retired_assets,
            "expired_licenses": expired_licenses
        }