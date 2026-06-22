from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class AssetBase(BaseModel):
    asset_tag: str
    name: str
    asset_type: str
    brand: str | None = None
    model: str | None = None
    serial_number: str
    purchase_date: date | None = None
    status: str = "AVAILABLE"
    location: str | None = None
    notes: str | None = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    asset_tag: str | None = None
    name: str | None = None
    asset_type: str | None = None
    brand: str | None = None
    model: str | None = None
    serial_number: str | None = None
    purchase_date: date | None = None
    status: str | None = None
    location: str | None = None
    notes: str | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class AssetRead(AssetBase):
    id: int
    assigned_user_id: int | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )