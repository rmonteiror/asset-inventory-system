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


class Asset(Base):
    __tablename__ = "assets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    asset_tag = Column(
        String(50),
        unique=True,
        nullable=False
    )

    name = Column(
        String(255),
        nullable=False
    )

    asset_type = Column(
        String(50),
        nullable=False
    )

    brand = Column(
        String(100),
        nullable=True
    )

    model = Column(
        String(100),
        nullable=True
    )

    serial_number = Column(
        String(255),
        unique=True,
        nullable=False
    )

    purchase_date = Column(
        Date,
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False,
        default="AVAILABLE"
    )

    location = Column(
        String(255),
        nullable=True
    )

    assigned_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    notes = Column(
        String(1000),
        nullable=True
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

    assigned_user = relationship(
        "User",
        back_populates="assets"
    )

    licenses = relationship(
        "License",
        back_populates="asset",
        cascade="all, delete-orphan"
    )

    maintenances = relationship(
        "Maintenance",
        back_populates="asset",
        cascade="all, delete-orphan"
    )