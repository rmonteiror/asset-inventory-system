from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    serial_number = Column(String(255), unique=True, nullable=False)
    category = Column(String(100), nullable=False)
    location = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
