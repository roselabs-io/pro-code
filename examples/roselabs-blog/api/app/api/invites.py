from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin
from app.core.db import get_session
from app.core.security import create_access_token
from app.models.author import Author
from app.schemas.auth import TokenResponse
from app.schemas.invitation import InviteAccept, InviteCreate
from app.services.invitations import InvitationService

router = APIRouter(tags=["invites"])


@router.post("/invites", status_code=status.HTTP_201_CREATED)
async def create_invite(
    body: InviteCreate,
    admin: Author = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    await InvitationService(session).invite(admin, body.email)
    return {"status": "sent"}


@router.post("/invites/accept", response_model=TokenResponse)
async def accept_invite(
    body: InviteAccept,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    author = await InvitationService(session).accept(
        body.token, body.display_name, body.password
    )
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired invitation",
        )
    return TokenResponse(access_token=create_access_token(str(author.id)))
