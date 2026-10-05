from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth import router as auth_router
from .config import settings

app = FastAPI(title="Agentic Telegram Bot Builder API", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.backend_cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth_router, prefix="/api/v1")

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/api/v1/health")
async def api_health() -> dict[str, str]:
    return {"status": "ok"}
