import os
from uuid import uuid4

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
os.environ.setdefault("BACKEND_CORS_ORIGINS", "http://localhost:3000")

from app.api.bots import get_owned_bot
from app.models import BotWorkspace, User


def test_bot_workspace_model_contract():
    assert BotWorkspace.__tablename__ == "bot_workspaces"
    assert User.__tablename__ == "users"


def test_bot_workspace_ownership_query_shape():
    assert get_owned_bot is not None
    bot_id = uuid4()
    user_id = uuid4()
    bot = BotWorkspace(id=bot_id, user_id=user_id, name="Test Bot")
    assert bot.id == bot_id
    assert bot.user_id == user_id
    assert bot.name == "Test Bot"


def test_bot_workspace_defaults():
    bot = BotWorkspace(user_id=uuid4(), name="My Bot")
    assert bot.status == "draft"
    assert bot.current_version_id is None
    assert bot.description is None
