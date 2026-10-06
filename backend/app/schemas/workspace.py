from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    bot_workspace_id: UUID
    created_at: datetime
    updated_at: datetime
class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    metadata_: dict | None
    created_at: datetime
class VersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    bot_workspace_id: UUID
    version_number: int
    source_reference: str | None
    change_description: str | None
    status: str
    test_status: str
    created_at: datetime
