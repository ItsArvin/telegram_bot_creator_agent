from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..config import settings
from ..database import get_db
from ..models import User
from ..services.session import get_user_from_token
async def get_current_user(session_token: str | None = Cookie(default=None, alias=settings.session_cookie_name), db: AsyncSession = Depends(get_db)) -> User:
    user = await get_user_from_token(db, session_token)
    if user is None: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return user
