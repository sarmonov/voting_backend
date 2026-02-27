from app.db.database import engine
from app.db.base import Base
from app.models import user, candidate, region  # noqa: F401


def init_db():
    Base.metadata.create_all(bind=engine)
