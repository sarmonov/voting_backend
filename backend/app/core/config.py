import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/voting_db")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme-super-secret-key-32chars")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # Blockchain
    GANACHE_URL: str = os.getenv("GANACHE_URL", "http://127.0.0.1:7545")
    CONTRACT_ADDRESS: str = os.getenv("CONTRACT_ADDRESS", "")


settings = Settings()
