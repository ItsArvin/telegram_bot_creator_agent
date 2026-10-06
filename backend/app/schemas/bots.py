from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
class BotCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=5000)
class BotUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=5000)
class BotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    description: str | None
    status: str
    current_version_id: UUID | None
    created_at: datetime
    updated_at: datetime
class BotListResponse(BaseModel):
    items: list[BotResponse]
    total: int
