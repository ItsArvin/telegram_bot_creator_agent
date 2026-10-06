from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import BotWorkspace, User
from ..schemas.bots import BotCreate, BotListResponse, BotResponse, BotUpdate
from .dependencies import get_current_user
router = APIRouter(prefix="/bots", tags=["bots"])
async def get_owned_bot(bot_id: UUID, user: User, db: AsyncSession) -> BotWorkspace:
    bot = await db.scalar(select(BotWorkspace).where(BotWorkspace.id == bot_id, BotWorkspace.user_id == user.id))
    if bot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bot workspace not found")
    return bot
@router.get("", response_model=BotListResponse)
async def list_bots(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> BotListResponse:
    items = list((await db.scalars(select(BotWorkspace).where(BotWorkspace.user_id == user.id).order_by(BotWorkspace.updated_at.desc()))).all())
    return BotListResponse(items=items, total=len(items))
@router.post("", response_model=BotResponse, status_code=status.HTTP_201_CREATED)
async def create_bot(payload: BotCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> BotWorkspace:
    bot = BotWorkspace(user_id=user.id, name=payload.name.strip(), description=payload.description)
    db.add(bot)
    await db.commit()
    await db.refresh(bot)
    return bot
@router.get("/{bot_id}", response_model=BotResponse)
async def get_bot(bot_id: UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> BotWorkspace:
    return await get_owned_bot(bot_id, user, db)
@router.patch("/{bot_id}", response_model=BotResponse)
async def update_bot(bot_id: UUID, payload: BotUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> BotWorkspace:
    bot = await get_owned_bot(bot_id, user, db)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(bot, key, value.strip() if isinstance(value, str) and key == "name" else value)
    await db.commit()
    await db.refresh(bot)
    return bot
@router.delete("/{bot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bot(bot_id: UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> None:
    bot = await get_owned_bot(bot_id, user, db)
    await db.delete(bot)
    await db.commit()
