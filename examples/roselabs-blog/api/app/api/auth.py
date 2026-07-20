from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_author
from app.core.db import get_session
from app.core.log import log_event
from app.core.security import create_access_token
from app.models.author import Author
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.author import AuthorOut
from app.services.auth import AuthService

router = APIRouter(tags=["auth"])


@router.post("/auth/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    author = await AuthService(session).authenticate(body.email, body.password)
    if author is None:
        log_event("AUTH_DENIED", reason="bad_credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return TokenResponse(access_token=create_access_token(str(author.id)))


@router.get("/auth/me", response_model=AuthorOut)
async def me(current: Author = Depends(get_current_author)) -> Author:
    return current
