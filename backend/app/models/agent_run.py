from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class AgentRun(Base):
    __tablename__ = "agent_runs"
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    bot_workspace_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("bot_workspaces.id", ondelete="CASCADE"), index=True, nullable=False)
    message_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("messages.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending", server_default="pending")
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
