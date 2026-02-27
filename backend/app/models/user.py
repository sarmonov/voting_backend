from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    passport_serial = Column(String, unique=True, index=True)
    pinfl = Column(String, unique=True, index=True) # JSHSHIR
    
    # Hududlar bilan bog'liqlik
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    
    # Blokcheyn va xavfsizlik
    wallet_address = Column(String, unique=True) # Ganache hamyon manzili
    hashed_password = Column(String, nullable=True)
    is_voted = Column(Boolean, default=False)
