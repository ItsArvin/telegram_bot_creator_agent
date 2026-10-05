import os
os.environ.setdefault("DATABASE_URL","postgresql+asyncpg://test:test@localhost/test")
os.environ.setdefault("BACKEND_CORS_ORIGINS","http://localhost:3000")
from fastapi.testclient import TestClient
from app.main import app
def test_health():
    r=TestClient(app).get("/health");assert r.status_code==200;assert r.json()=={"status":"ok"}
def test_api_health():
    r=TestClient(app).get("/api/v1/health");assert r.status_code==200;assert r.json()=={"status":"ok"}
