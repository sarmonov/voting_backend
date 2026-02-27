from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateRead, CandidateCreate
from app.services.blockchain_service import BlockchainService

router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.get("/", response_model=List[CandidateRead])
def get_candidates(db: Session = Depends(get_db)):
    candidates = db.query(Candidate).all()
    for c in candidates:
        c.vote_count = BlockchainService.get_candidate_votes(c.id)
    return candidates


@router.post("/", response_model=CandidateRead, status_code=201)
def create_candidate(data: CandidateCreate, db: Session = Depends(get_db)):
    candidate = Candidate(**data.dict())
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate
