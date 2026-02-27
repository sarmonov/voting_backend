from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from app.services.blockchain_service import BlockchainService


class UserService:
    @staticmethod
    def get_by_pinfl(db: Session, pinfl: str) -> Optional[User]:
        return db.query(User).filter(User.pinfl == pinfl).first()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all(db: Session) -> List[User]:
        return db.query(User).all()

    @staticmethod
    def create(db: Session, data: UserCreate) -> User:
        if UserService.get_by_pinfl(db, data.pinfl):
            raise HTTPException(status_code=400, detail="Bu PINFL bilan foydalanuvchi allaqachon mavjud")
        if db.query(User).filter(User.passport_serial == data.passport_serial).first():
            raise HTTPException(status_code=400, detail="Bu passport seriyasi allaqachon royxatdan otgan")
        try:
            users_count = db.query(User).count()
            wallet = BlockchainService.get_free_wallet(users_count)
        except ValueError:
            wallet = None
        new_user = User(
            full_name=data.full_name,
            passport_serial=data.passport_serial,
            pinfl=data.pinfl,
            hashed_password=get_password_hash(data.password),
            region_id=data.region_id,
            district_id=data.district_id,
            wallet_address=wallet,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def authenticate(db: Session, pinfl: str, password: str) -> Optional[User]:
        user = UserService.get_by_pinfl(db, pinfl)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
