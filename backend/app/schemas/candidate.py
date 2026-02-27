from pydantic import BaseModel
from typing import Optional


class CandidateCreate(BaseModel):
    name: str
    party: Optional[str] = None
    bio: Optional[str] = None
    photo_url: Optional[str] = None


class CandidateRead(BaseModel):
    id: int
    name: str
    party: Optional[str]
    bio: Optional[str]
    photo_url: Optional[str]
    vote_count: int

    class Config:
        from_attributes = True
