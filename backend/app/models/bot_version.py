from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base

class BotVersion(Base):
    __tablename__ = "bot_versions"
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    bot_workspace_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("bot_workspaces.id", ondelete="CASCADE"), index=True, nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    source_reference: Mapped[str | None] = mapped_column(String(512), nullable=True)
    change_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft", server_default="draft")
    test_status: Mapped[str] = mapped_column(String(32), nullable=False, default="not_run", server_default="not_run")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    bot_workspace: Mapped["BotWorkspace"] = relationship(back_populates="versions", foreign_keys=[bot_workspace_id])
