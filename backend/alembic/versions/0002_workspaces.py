"""add bot workspace persistence"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = "0002_workspaces"
down_revision = "0001_auth"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("bot_workspaces", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("name", sa.String(160), nullable=False), sa.Column("description", sa.Text(), nullable=True), sa.Column("status", sa.String(32), server_default="draft", nullable=False), sa.Column("current_version_id", postgresql.UUID(as_uuid=True), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_bot_workspaces_user_id", "bot_workspaces", ["user_id"])
    op.create_index("ix_bot_workspaces_updated_at", "bot_workspaces", ["updated_at"])
    op.create_table("conversations", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("bot_workspace_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.ForeignKeyConstraint(["bot_workspace_id"], ["bot_workspaces.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_conversations_bot_workspace_id", "conversations", ["bot_workspace_id"])
    op.create_table("messages", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("conversation_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("role", sa.String(24), nullable=False), sa.Column("content", sa.Text(), nullable=False), sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_messages_conversation_id", "messages", ["conversation_id"])
    op.create_table("bot_versions", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("bot_workspace_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("version_number", sa.Integer(), nullable=False), sa.Column("source_reference", sa.String(512), nullable=True), sa.Column("change_description", sa.Text(), nullable=True), sa.Column("status", sa.String(32), server_default="draft", nullable=False), sa.Column("test_status", sa.String(32), server_default="not_run", nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.ForeignKeyConstraint(["bot_workspace_id"], ["bot_workspaces.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("bot_workspace_id", "version_number", name="uq_bot_versions_workspace_number"))
    op.create_index("ix_bot_versions_bot_workspace_id", "bot_versions", ["bot_workspace_id"])
    op.create_table("sandbox_runs", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("bot_version_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("sandbox_reference", sa.String(512), nullable=True), sa.Column("status", sa.String(32), server_default="pending", nullable=False), sa.Column("started_at", sa.DateTime(timezone=True), nullable=True), sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True), sa.Column("error_message", sa.Text(), nullable=True), sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True), sa.ForeignKeyConstraint(["bot_version_id"], ["bot_versions.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_sandbox_runs_bot_version_id", "sandbox_runs", ["bot_version_id"])
    op.create_table("test_runs", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("sandbox_run_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("test_type", sa.String(64), nullable=False), sa.Column("status", sa.String(32), server_default="pending", nullable=False), sa.Column("output", sa.Text(), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.ForeignKeyConstraint(["sandbox_run_id"], ["sandbox_runs.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_test_runs_sandbox_run_id", "test_runs", ["sandbox_run_id"])
    op.create_table("agent_runs", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("bot_workspace_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("message_id", postgresql.UUID(as_uuid=True), nullable=True), sa.Column("status", sa.String(32), server_default="pending", nullable=False), sa.Column("started_at", sa.DateTime(timezone=True), nullable=True), sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True), sa.Column("error_message", sa.Text(), nullable=True), sa.ForeignKeyConstraint(["bot_workspace_id"], ["bot_workspaces.id"], ondelete="CASCADE"), sa.ForeignKeyConstraint(["message_id"], ["messages.id"], ondelete="SET NULL"), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_agent_runs_bot_workspace_id", "agent_runs", ["bot_workspace_id"])
    op.create_index("ix_agent_runs_message_id", "agent_runs", ["message_id"])
    op.create_table("agent_events", sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("agent_run_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("event_type", sa.String(64), nullable=False), sa.Column("message", sa.Text(), nullable=False), sa.Column("step", sa.String(64), nullable=True), sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.ForeignKeyConstraint(["agent_run_id"], ["agent_runs.id"], ondelete="CASCADE"), sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_agent_events_agent_run_id", "agent_events", ["agent_run_id"])

def downgrade():
    for index_name, table_name in [("ix_agent_events_agent_run_id","agent_events"),("ix_agent_runs_message_id","agent_runs"),("ix_agent_runs_bot_workspace_id","agent_runs"),("ix_test_runs_sandbox_run_id","test_runs"),("ix_sandbox_runs_bot_version_id","sandbox_runs"),("ix_bot_versions_bot_workspace_id","bot_versions"),("ix_messages_conversation_id","messages"),("ix_conversations_bot_workspace_id","conversations")]:
        op.drop_index(index_name, table_name=table_name)
    for table in ["agent_events", "agent_runs", "test_runs", "sandbox_runs", "bot_versions", "messages", "conversations"]: op.drop_table(table)
    op.drop_index("ix_bot_workspaces_updated_at", table_name="bot_workspaces")
    op.drop_index("ix_bot_workspaces_user_id", table_name="bot_workspaces")
    op.drop_table("bot_workspaces")
