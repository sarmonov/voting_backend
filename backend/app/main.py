from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import AppException, app_exception_handler
from app.api.routers import auth, users, candidates, vote, regions
from app.db.init_db import init_db

app = FastAPI(
    title="Blokcheyn Saylov Tizimi",
    description=(
        "O'\''zbekiston saylov tizimi backenidi. "
        "**Kirish uchun:** `/auth/login` orqali PINFL va parol bilan token oling, "
        "so'\''ng Swagger UI'\''dagi **Authorize** tugmasi orqali Bearer token kiriting."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(candidates.router)
app.include_router(vote.router)
app.include_router(regions.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Blokcheyn Saylov Tizimiga Xush Kelibsiz!", "docs": "/docs"}
