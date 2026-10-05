from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"
    database_url: str
    auth_secret: str = "change-me-in-development"
    encryption_key: str = "change-me-in-development"
    session_days: int = 7
    session_cookie_name: str = "atbb_session"
    # Keep this as a plain string because Pydantic Settings parses list fields
    # as JSON before field validators run. Vercel stores environment variables
    # as strings, so comma-separated origins are easier and more robust here.
    backend_cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> list[str]:
        configured = [origin.strip().rstrip("/") for origin in self.backend_cors_origins.split(",") if origin.strip()]
        frontend_origin = "https://telegram-bot-creator-frontend.vercel.app"
        return list(dict.fromkeys([*configured, frontend_origin]))


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
