import os
from uuid import uuid4

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
os.environ.setdefault("BACKEND_CORS_ORIGINS", "http://localhost:3000")
os.environ.setdefault("ENCRYPTION_KEY", "test-encryption-key")

from app.models import BotWorkspace, TelegramCredential
from app.services.telegram import decrypt_token, encrypt_token


def test_telegram_credential_contract():
    bot_id = uuid4()
    credential = TelegramCredential(
        bot_workspace_id=bot_id,
        encrypted_token=encrypt_token("123456789:AAabcdefghijklmnopqrstuvwxyz"),
        telegram_bot_id=123456789,
        telegram_username="example_bot",
    )
    assert credential.bot_workspace_id == bot_id
    assert credential.telegram_bot_id == 123456789
    assert credential.telegram_username == "example_bot"


def test_token_round_trip_encryption():
    token = "123456789:AAabcdefghijklmnopqrstuvwxyz"
    encrypted = encrypt_token(token)
    assert encrypted != token
    assert decrypt_token(encrypted) == token


def test_workspace_has_telegram_relationship():
    assert hasattr(BotWorkspace, "telegram_credential")
