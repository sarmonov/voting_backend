from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.vote import VoteRequest, VoteResponse
from app.services.voting_service import VotingService

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", response_model=VoteResponse)
def cast_vote(
    request: VoteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return VotingService.cast_vote(db=db, request=request, current_user=current_user)
