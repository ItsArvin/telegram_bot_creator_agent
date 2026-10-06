from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base

class BotWorkspace(Base):
    __tablename__ = "bot_workspaces"
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft", server_default="draft")
    current_version_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    user: Mapped["User"] = relationship(back_populates="bot_workspaces")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="bot_workspace", cascade="all, delete-orphan")
    versions: Mapped[list["BotVersion"]] = relationship(back_populates="bot_workspace", cascade="all, delete-orphan", foreign_keys="BotVersion.bot_workspace_id")
    telegram_credential: Mapped["TelegramCredential | None"] = relationship(back_populates="bot_workspace", uselist=False, cascade="all, delete-orphan")
