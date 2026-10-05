from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    environment: str = "development"
    database_url: str
    auth_secret: str = "change-me-in-development"
    encryption_key: str = "change-me-in-development"
    session_days: int = 7
    session_cookie_name: str = "atbb_session"
    backend_cors_origins: list[str] = ["http://localhost:3000"]
    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_origins(cls, value):
        if isinstance(value, str): return [x.strip() for x in value.split(",") if x.strip()]
        return value
@lru_cache
def get_settings(): return Settings()
settings = get_settings()
