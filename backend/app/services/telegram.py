from typing import Any

import httpx
from cryptography.fernet import Fernet

from ..config import settings


def _fernet() -> Fernet:
    # Derive a stable Fernet key from the configured application secret.
    import base64
    import hashlib

    key = base64.urlsafe_b64encode(hashlib.sha256(settings.encryption_key.encode()).digest())
    return Fernet(key)


def encrypt_token(token: str) -> str:
    return _fernet().encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    return _fernet().decrypt(encrypted_token.encode()).decode()


async def verify_telegram_token(token: str) -> dict[str, Any]:
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            data = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise ValueError("Could not reach Telegram to verify the token") from exc

    if response.status_code != 200 or not data.get("ok") or not data.get("result"):
        raise ValueError("Invalid Telegram bot token")

    return data["result"]
