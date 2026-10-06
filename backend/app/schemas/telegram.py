from pydantic import BaseModel, Field


class TelegramConnectRequest(BaseModel):
    token: str = Field(min_length=20, max_length=256)


class TelegramStatusResponse(BaseModel):
    connected: bool
    telegram_bot_id: int | None = None
    username: str | None = None
    first_name: str | None = None
