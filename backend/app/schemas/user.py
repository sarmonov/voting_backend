from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    full_name: str
    passport_serial: str
    pinfl: str
    password: str
    region_id: Optional[int] = None
    district_id: Optional[int] = None


class UserRead(BaseModel):
    id: int
    full_name: str
    passport_serial: str
    pinfl: str
    region_id: Optional[int]
    district_id: Optional[int]
    wallet_address: Optional[str]
    is_voted: bool
    is_active: bool

    class Config:
        from_attributes = True


class UserInDB(UserRead):
    hashed_password: str
