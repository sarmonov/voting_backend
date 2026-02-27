from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, blockchain
from .database import engine, get_db

# Jadvallarni yaratish
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blokcheyn Saylov Tizimi")

@app.get("/candidates/", response_model=List[schemas.Candidate])
def get_candidates(db: Session = Depends(get_db)):
    candidates = db.query(models.Candidate).all()
    for c in candidates:
        # Har bir nomzod ovozini blokcheyndan yangilab olamiz
        c.vote_count = blockchain.get_candidate_votes_from_bc(c.id)
    return candidates

@app.post("/register/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # PINFL bo'yicha tekshirish
    db_user = db.query(models.User).filter(models.User.pinfl == user.pinfl).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Foydalanuvchi allaqachon mavjud")
    
    # Ganache hamyonlaridan birini biriktirish
    users_count = db.query(models.User).count()
    wallet = blockchain.w3.eth.accounts[users_count + 1] # 0-indeks admin/deployer uchun
    
    new_user = models.User(**user.dict(), wallet_address=wallet)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/vote/")
def vote(request: schemas.VoteRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.wallet_address == request.voter_wallet).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    if user.is_voted:
        raise HTTPException(status_code=400, detail="Siz ovoz berib bo'lgansiz")

    # Blokcheynga yozish
    success = blockchain.vote_in_blockchain(request.candidate_id, user.wallet_address)
    if success:
        user.is_voted = True
        db.commit()
        return {"message": "Ovozingiz muvaffaqiyatli qabul qilindi!"}
    
    raise HTTPException(status_code=500, detail="Blokcheyn xatosi")