from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    party = Column(String(200), nullable=True)
    bio = Column(String(1000), nullable=True)    # Qisqacha tarjimai hol
    photo_url = Column(String(500), nullable=True)
    vote_count = Column(Integer, default=0)      # Cache — asl ovoz blokcheynda
