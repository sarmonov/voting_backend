from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateRead, CandidateCreate
from app.services.blockchain_service import BlockchainService

router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.get("/", response_model=List[CandidateRead], summary="Barcha nomzodlar ro'yxati")
def get_candidates(db: Session = Depends(get_db)):
    """
    Nomzodlar ro'yxatini qaytaradi.  
    Har bir nomzodning `vote_count` blokcheyndan yangilanib kelinadi.
    """
    candidates = db.query(Candidate).all()
    for c in candidates:
        c.vote_count = BlockchainService.get_candidate_votes(c.id)
    return candidates


@router.post("/", response_model=CandidateRead, status_code=201,
             summary="Yangi nomzod qo'shish (Admin)")
def create_candidate(data: CandidateCreate, db: Session = Depends(get_db)):
    """Yangi saylov nomzodini bazaga qo'shadi."""
    candidate = Candidate(**data.dict())
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate
