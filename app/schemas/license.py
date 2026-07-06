from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class LicenseBase(BaseModel):
    software_name: str
    vendor: str
    license_key: str
    version: str | None = None
    expiration_date: date | None = None
    status: str = "ACTIVE"
    asset_id: int


class LicenseCreate(LicenseBase):
    pass


class LicenseUpdate(BaseModel):
    software_name: str | None = None
    vendor: str | None = None
    license_key: str | None = None
    version: str | None = None
    expiration_date: date | None = None
    status: str | None = None
    asset_id: int | None = None


class LicenseRead(LicenseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )