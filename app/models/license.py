from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.base import Base


class License(Base):
    __tablename__ = "licenses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    software_name = Column(
        String(255),
        nullable=False
    )

    vendor = Column(
        String(255),
        nullable=False
    )

    license_key = Column(
        String(255),
        unique=True,
        nullable=False
    )

    version = Column(
        String(100),
        nullable=True
    )

    expiration_date = Column(
        Date,
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False,
        default="ACTIVE"
    )

    asset_id = Column(
        Integer,
        ForeignKey("assets.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    asset = relationship(
        "Asset",
        back_populates="licenses"
    )