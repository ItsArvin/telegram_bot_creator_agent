from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.auth import router as auth_router
from .api.bots import router as bots_router
from .api.telegram import router as telegram_router
from .config import settings
from .database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.auto_create_tables:
        from . import models  # noqa: F401
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Agentic Telegram Bot Builder API", version="0.5.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth_router, prefix="/api/v1")
app.include_router(bots_router, prefix="/api/v1")
app.include_router(telegram_router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/health")
async def api_health() -> dict[str, str]:
    return {"status": "ok"}
