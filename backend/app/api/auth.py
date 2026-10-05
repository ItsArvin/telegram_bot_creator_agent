from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from ..config import settings
from ..database import get_db
from ..models import User
from ..schemas.auth import LoginRequest, RegisterRequest, UserResponse
from ..services.password import hash_password, verify_password
from ..services.session import create_session, delete_session
from .dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

def set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(key=settings.session_cookie_name, value=token, httponly=True,
        secure=settings.environment == "production", samesite="none" if settings.environment == "production" else "lax",
        max_age=settings.session_days * 24 * 60 * 60, path="/")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, response: Response, db: AsyncSession = Depends(get_db)) -> User:
    email = payload.email.lower().strip()
    if await db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = User(email=email, password_hash=hash_password(payload.password))
    db.add(user)
    try:
        await db.flush()
        token = await create_session(db, user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="An account with this email already exists") from None
    set_session_cookie(response, token)
    return user

@router.post("/login", response_model=UserResponse)
async def login(payload: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)) -> User:
    email = payload.email.lower().strip()
    user = await db.scalar(select(User).where(User.email == email))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = await create_session(db, user)
    set_session_cookie(response, token)
    return user

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response, session_token: str | None = Cookie(default=None), db: AsyncSession = Depends(get_db)) -> None:
    await delete_session(db, session_token)
    response.delete_cookie(key=settings.session_cookie_name, path="/")

@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
