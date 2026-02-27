"""Writes all backend module files that ended up empty on disk."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(BASE, "app")


def w(rel_path, content):
    full = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  OK  {rel_path}  ({len(content)} chars)")


# ── db ────────────────────────────────────────────────────────────────────────

w("app/db/base.py", """\
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
""")

w("app/db/database.py", """\
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base  # noqa

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
""")

w("app/db/init_db.py", """\
from app.db.database import engine
from app.db.base import Base
from app.models import user, candidate, region  # noqa: F401


def init_db():
    Base.metadata.create_all(bind=engine)
""")

# ── models ────────────────────────────────────────────────────────────────────

w("app/models/user.py", """\
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    passport_serial = Column(String(20), unique=True, index=True, nullable=False)
    pinfl = Column(String(14), unique=True, index=True, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    wallet_address = Column(String(42), unique=True, nullable=True)
    is_voted = Column(Boolean, default=False)
""")

w("app/models/candidate.py", """\
from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    party = Column(String(200), nullable=True)
    bio = Column(String(1000), nullable=True)
    photo_url = Column(String(500), nullable=True)
    vote_count = Column(Integer, default=0)
""")

w("app/models/region.py", """\
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, index=True, nullable=False)
    districts = relationship("District", back_populates="region", cascade="all, delete-orphan")


class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    region = relationship("Region", back_populates="districts")
""")

w("app/models/__init__.py", """\
from app.models.user import User
from app.models.candidate import Candidate
from app.models.region import Region, District

__all__ = ["User", "Candidate", "Region", "District"]
""")

# ── schemas ───────────────────────────────────────────────────────────────────

w("app/schemas/user.py", """\
from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    full_name: str
    passport_serial: str
    pinfl: str
    password: str
    region_id: Optional[int] = None
    district_id: Optional[int] = None


class UserRead(BaseModel):
    id: int
    full_name: str
    passport_serial: str
    pinfl: str
    region_id: Optional[int]
    district_id: Optional[int]
    wallet_address: Optional[str]
    is_voted: bool
    is_active: bool

    class Config:
        from_attributes = True
""")

w("app/schemas/candidate.py", """\
from pydantic import BaseModel
from typing import Optional


class CandidateCreate(BaseModel):
    name: str
    party: Optional[str] = None
    bio: Optional[str] = None
    photo_url: Optional[str] = None


class CandidateRead(BaseModel):
    id: int
    name: str
    party: Optional[str]
    bio: Optional[str]
    photo_url: Optional[str]
    vote_count: int

    class Config:
        from_attributes = True
""")

w("app/schemas/vote.py", """\
from pydantic import BaseModel


class VoteRequest(BaseModel):
    candidate_id: int


class VoteResponse(BaseModel):
    message: str
    tx_status: bool
""")

w("app/schemas/auth.py", """\
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    pinfl: Optional[str] = None
""")

w("app/schemas/__init__.py", """\
from app.schemas.user import UserCreate, UserRead
from app.schemas.candidate import CandidateCreate, CandidateRead
from app.schemas.vote import VoteRequest, VoteResponse
from app.schemas.auth import Token, TokenData

__all__ = ["UserCreate", "UserRead", "CandidateCreate", "CandidateRead",
           "VoteRequest", "VoteResponse", "Token", "TokenData"]
""")

# ── services ──────────────────────────────────────────────────────────────────

w("app/services/blockchain_service.py", """\
import json
from web3 import Web3
from app.core.config import settings

w3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))

ABI = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"_candidateId","type":"uint256"}],"name":"votedEvent","type":"event"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"candidates","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"voteCount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"candidatesCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_candidateId","type":"uint256"}],"name":"vote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"voters","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')


def _get_contract():
    if not settings.CONTRACT_ADDRESS:
        return None
    return w3.eth.contract(address=settings.CONTRACT_ADDRESS, abi=ABI)


class BlockchainService:
    @staticmethod
    def is_connected():
        return w3.is_connected()

    @staticmethod
    def get_free_wallet(users_count: int) -> str:
        accounts = w3.eth.accounts
        index = users_count + 1
        if index >= len(accounts):
            raise ValueError("Ganache'da bosh hamyon yoq!")
        return accounts[index]

    @staticmethod
    def vote_in_blockchain(candidate_id: int, voter_address: str) -> bool:
        contract = _get_contract()
        if not contract:
            print("OGOHLANTIRISH: CONTRACT_ADDRESS yoq.")
            return True
        try:
            tx_hash = contract.functions.vote(candidate_id).transact({"from": voter_address})
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            return receipt.status == 1
        except Exception as e:
            print(f"Blokcheyn xatosi: {e}")
            return False

    @staticmethod
    def get_candidate_votes(candidate_id: int) -> int:
        contract = _get_contract()
        if not contract:
            return 0
        try:
            candidate = contract.functions.candidates(candidate_id).call()
            return candidate[2]
        except Exception:
            return 0
""")

w("app/services/user_service.py", """\
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
""")

w("app/services/voting_service.py", """\
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
""")

w("app/services/auth_service.py", """\
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
        user: Optional[User] = UserService.authenticate(db, pinfl, password)
        if not user:
            raise HTTPException(status_code=401, detail="PINFL yoki parol notogri",
                                headers={"WWW-Authenticate": "Bearer"})
        if not user.is_active:
            raise HTTPException(status_code=403, detail="Hisobingiz faol emas")
        access_token = create_access_token(data={"sub": user.pinfl})
        return Token(access_token=access_token, token_type="bearer")
""")

# ── api/routers ───────────────────────────────────────────────────────────────

w("app/api/routers/auth.py", """\
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.auth import Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token, summary="Tizimga kirish (JWT token olish)")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return AuthService.login(db=db, pinfl=form_data.username, password=form_data.password)
""")

w("app/api/routers/users.py", """\
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserRead, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return UserService.create(db=db, data=user_data)


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
""")

w("app/api/routers/candidates.py", """\
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
""")

w("app/api/routers/vote.py", """\
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
""")

w("app/api/routers/regions.py", """\
from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.models.region import Region

router = APIRouter(prefix="/regions", tags=["Regions"])


class DistrictRead(BaseModel):
    id: int
    name: str
    region_id: int
    class Config:
        from_attributes = True


class RegionRead(BaseModel):
    id: int
    name: str
    districts: List[DistrictRead] = []
    class Config:
        from_attributes = True


@router.get("/", response_model=List[RegionRead])
def get_regions(db: Session = Depends(get_db)):
    return db.query(Region).all()
""")

print("\nAll files written successfully!")
