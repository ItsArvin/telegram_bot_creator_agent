def test_phase2_models_import():
    from app.models import AgentEvent, AgentRun, BotVersion, BotWorkspace, Conversation, Message, SandboxRun, TestRun
    assert all([AgentEvent, AgentRun, BotVersion, BotWorkspace, Conversation, Message, SandboxRun, TestRun])

def test_bot_schema():
    from app.schemas.bots import BotCreate, BotUpdate
    payload=BotCreate(name=" Demo Bot ", description="test")
    assert payload.name == " Demo Bot "
    assert BotUpdate(name="Updated").name == "Updated"

def test_bot_router_registered():
    from app.main import app
    paths={route.path for route in app.routes}
    assert "/api/v1/bots" in paths
    assert "/api/v1/bots/{bot_id}" in paths
