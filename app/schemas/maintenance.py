from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class MaintenanceBase(BaseModel):
    asset_id: int
    title: str
    description: str | None = None
    maintenance_type: str
    status: str = "OPEN"
    technician: str | None = None
    cost: float | None = None
    start_date: date
    end_date: date | None = None


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    maintenance_type: str | None = None
    status: str | None = None
    technician: str | None = None
    cost: float | None = None
    start_date: date | None = None
    end_date: date | None = None
    asset_id: int | None = None


class MaintenanceRead(MaintenanceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )