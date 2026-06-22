from pydantic import BaseModel

class AssetBase(BaseModel):
    name: str
    serial_number: str
    category: str
    location: str | None = None
    notes: str | None = None

class AssetCreate(AssetBase):
    pass

class AssetRead(AssetBase):
    id: int

    class Config:
        orm_mode = True
