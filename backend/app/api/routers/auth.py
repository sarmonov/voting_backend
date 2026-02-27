from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.auth import Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token, summary="Tizimga kirish (JWT token olish)")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    PINFL → `username` maydoniga, parol → `password` maydoniga kiritiladi.
    Muvaffaqiyatli bo'lsa JWT access token qaytaradi.
    """
    # OAuth2PasswordRequestForm: username=pinfl, password=parol
    return AuthService.login(db=db, pinfl=form_data.username, password=form_data.password)
