"""add encrypted Telegram credentials

Revision ID: 0003_telegram_credentials
Revises: 0002_bot_workspaces
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0003_telegram_credentials"
down_revision = "0002_bot_workspaces"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "telegram_credentials",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("bot_workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("encrypted_token", sa.String(1024), nullable=False),
        sa.Column("telegram_bot_id", sa.BigInteger(), nullable=False),
        sa.Column("telegram_username", sa.String(64), nullable=True),
        sa.Column("telegram_first_name", sa.String(256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["bot_workspace_id"], ["bot_workspaces.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("bot_workspace_id", name="uq_telegram_credentials_workspace"),
    )
    op.create_index("ix_telegram_credentials_bot_workspace_id", "telegram_credentials", ["bot_workspace_id"])


def downgrade():
    op.drop_index("ix_telegram_credentials_bot_workspace_id", table_name="telegram_credentials")
    op.drop_table("telegram_credentials")
