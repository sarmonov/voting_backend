from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    passport_serial = Column(String(20), unique=True, index=True, nullable=False)
    pinfl = Column(String(14), unique=True, index=True, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    wallet_address = Column(String(42), unique=True, nullable=True)
    is_voted = Column(Boolean, default=False)
