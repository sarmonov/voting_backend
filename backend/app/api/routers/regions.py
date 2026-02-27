from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.models.region import Region

router = APIRouter(prefix="/regions", tags=["Regions"])


class DistrictRead(BaseModel):
    id: int
    name: str
    region_id: int
    class Config:
        from_attributes = True


class RegionRead(BaseModel):
    id: int
    name: str
    districts: List[DistrictRead] = []
    class Config:
        from_attributes = True


@router.get("/", response_model=List[RegionRead])
def get_regions(db: Session = Depends(get_db)):
    return db.query(Region).all()
