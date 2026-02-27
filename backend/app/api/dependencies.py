from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.core.security import decode_access_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    """Har bir so'rov uchun DB sessiyasini beradi"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """JWT tokendan joriy foydalanuvchini topib beradi"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token noto'g'ri yoki muddati o'tgan",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    pinfl: str = payload.get("sub")
    if pinfl is None:
        raise credentials_exception

    user = db.query(User).filter(User.pinfl == pinfl).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Hisobingiz faol emas")

    return user
