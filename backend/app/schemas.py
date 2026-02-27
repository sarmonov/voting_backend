from pydantic import BaseModel
from typing import List, Optional

class CandidateBase(BaseModel):
    name: str
    party: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    id: int
    vote_count: int

    class Config:
        from_attributes = True

class VoteRequest(BaseModel):
    candidate_id: int
    voter_wallet: str

class UserBase(BaseModel):
    full_name: str
    passport_serial: str
    pinfl: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    wallet_address: Optional[str]
    is_voted: bool

    class Config:
        from_attributes = True