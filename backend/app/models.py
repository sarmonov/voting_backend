from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    districts = relationship("District", back_populates="region")

class District(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"))

    region = relationship("Region", back_populates="districts")

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    party = Column(String, nullable=True)
    vote_count = Column(Integer, default=0)

class User(Base):
    __tablename__ = "users"
    # SQLAlchemy xato bermasligi uchun quyidagi qatorni qo'shdik
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