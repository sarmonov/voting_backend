from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.vote import VoteRequest, VoteResponse
from app.services.blockchain_service import BlockchainService


class VotingService:
    @staticmethod
    def cast_vote(db: Session, request: VoteRequest, current_user: User) -> VoteResponse:
        if not current_user.is_active:
            raise HTTPException(status_code=403, detail="Hisobingiz faol emas")
        if current_user.is_voted:
            raise HTTPException(status_code=400, detail="Siz allaqachon ovoz bergansiz")
        if not current_user.wallet_address:
            raise HTTPException(status_code=400, detail="Sizga blokcheyn hamyoni biriktirilmagan")
        success = BlockchainService.vote_in_blockchain(request.candidate_id, current_user.wallet_address)
        if not success:
            raise HTTPException(status_code=500, detail="Blokcheynd xatolik yuz berdi")
        current_user.is_voted = True
        db.commit()
        return VoteResponse(message="Ovozingiz muvaffaqiyatli qabul qilindi!", tx_status=True)
