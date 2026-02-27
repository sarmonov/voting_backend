from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import create_access_token
from app.services.user_service import UserService
from app.schemas.auth import Token


class AuthService:

    @staticmethod
    def login(db: Session, pinfl: str, password: str) -> Token:
        """PINFL + parol orqali kirish va JWT token berish"""
        user: Optional[User] = UserService.authenticate(db, pinfl, password)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="PINFL yoki parol noto'g'ri",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(status_code=403, detail="Hisobingiz faol emas")

        access_token = create_access_token(data={"sub": user.pinfl})
        return Token(access_token=access_token, token_type="bearer")
