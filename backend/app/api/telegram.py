from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import BotWorkspace, TelegramCredential, User
from ..schemas.telegram import TelegramConnectRequest, TelegramStatusResponse
from ..services.telegram import encrypt_token, verify_telegram_token
from .bots import get_owned_bot
from .dependencies import get_current_user

router = APIRouter(prefix="/bots/{bot_id}/telegram", tags=["telegram"])


@router.get("", response_model=TelegramStatusResponse)
async def get_telegram_status(
    bot_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TelegramStatusResponse:
    await get_owned_bot(bot_id, user, db)
    credential = await db.scalar(
        select(TelegramCredential).where(TelegramCredential.bot_workspace_id == bot_id)
    )
    if credential is None:
        return TelegramStatusResponse(connected=False)
    return TelegramStatusResponse(
        connected=True,
        telegram_bot_id=credential.telegram_bot_id,
        username=credential.telegram_username,
        first_name=credential.telegram_first_name,
    )


@router.post("", response_model=TelegramStatusResponse)
async def connect_telegram(
    bot_id: UUID,
    payload: TelegramConnectRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TelegramStatusResponse:
    await get_owned_bot(bot_id, user, db)
    token = payload.token.strip()
    try:
        telegram_bot = await verify_telegram_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    credential = await db.scalar(
        select(TelegramCredential).where(TelegramCredential.bot_workspace_id == bot_id)
    )
    if credential is None:
        credential = TelegramCredential(bot_workspace_id=bot_id)
        db.add(credential)

    credential.encrypted_token = encrypt_token(token)
    credential.telegram_bot_id = int(telegram_bot["id"])
    credential.telegram_username = telegram_bot.get("username")
    credential.telegram_first_name = telegram_bot.get("first_name")
    await db.commit()
    await db.refresh(credential)

    return TelegramStatusResponse(
        connected=True,
        telegram_bot_id=credential.telegram_bot_id,
        username=credential.telegram_username,
        first_name=credential.telegram_first_name,
    )


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_telegram(
    bot_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    await get_owned_bot(bot_id, user, db)
    credential = await db.scalar(
        select(TelegramCredential).where(TelegramCredential.bot_workspace_id == bot_id)
    )
    if credential is not None:
        await db.delete(credential)
        await db.commit()
