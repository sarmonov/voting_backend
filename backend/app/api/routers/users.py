from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserRead, status_code=201,
             summary="Yangi foydalanuvchini ro'yxatdan o'tkazish")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Yangi saylovchi qayd qiladi.  
    Avtomatik Ganache hamyoni biriktiriladi.
    """
    return UserService.create(db=db, data=user_data)


@router.get("/me", response_model=UserRead, summary="Joriy foydalanuvchi ma'lumotlari")
def get_me(current_user: User = Depends(get_current_user)):
    """Tokendan foydalanuvchi ma'lumotini qaytaradi."""
    return current_user
