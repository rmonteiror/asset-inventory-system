from pydantic import BaseModel


class DashboardSummary(BaseModel):
    users: int
    assets: int
    licenses: int

    available_assets: int
    assigned_assets: int
    maintenance_assets: int
    retired_assets: int

    expired_licenses: int