import hashlib, secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..config import settings
from ..models import Session, User
def _hash_token(token: str) -> str: return hashlib.sha256(token.encode()).hexdigest()
def _utcnow(): return datetime.now(timezone.utc)
async def create_session(db: AsyncSession, user: User) -> str:
    raw = secrets.token_urlsafe(48)
    db.add(Session(user_id=user.id, token_hash=_hash_token(raw), expires_at=_utcnow()+timedelta(days=settings.session_days)))
    await db.commit()
    return raw
async def get_user_from_token(db: AsyncSession, raw_token: str | None) -> User | None:
    if not raw_token: return None
    row=(await db.execute(select(Session, User).join(User, User.id==Session.user_id).where(Session.token_hash==_hash_token(raw_token)))).first()
    if not row: return None
    session,user=row
    if session.expires_at <= _utcnow():
        await db.delete(session); await db.commit(); return None
    return user
async def delete_session(db: AsyncSession, raw_token: str | None) -> None:
    if not raw_token: return
    session=(await db.execute(select(Session).where(Session.token_hash==_hash_token(raw_token)))).scalar_one_or_none()
    if session: await db.delete(session); await db.commit()
