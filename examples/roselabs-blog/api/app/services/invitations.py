import datetime as dt
import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.log import log_event
from app.core.security import hash_password
from app.models.author import Author, Role
from app.models.invitation import Invitation
from app.repositories.authors import AuthorRepository
from app.repositories.invitations import InvitationRepository

INVITE_TTL = dt.timedelta(days=7)


class InvitationService:
    def __init__(self, session: AsyncSession) -> None:
        self.invites = InvitationRepository(session)
        self.authors = AuthorRepository(session)

    async def invite(self, inviter: Author, email: str) -> Invitation:
        token = secrets.token_urlsafe(24)
        invitation = Invitation(
            email=email,
            token=token,
            invited_by=inviter.id,
            expires_at=dt.datetime.now(dt.timezone.utc) + INVITE_TTL,
        )
        await self.invites.add(invitation)
        # Dev: log the email instead of sending it (Resend is wired at deploy, M7).
        log_event(
            "INVITE_EMAIL",
            to=email,
            accept_url=f"{settings.site_url}/accept-invite?token={token}",
        )
        return invitation

    async def accept(self, token: str, display_name: str, password: str) -> Author | None:
        invitation = await self.invites.get_by_token(token)
        now = dt.datetime.now(dt.timezone.utc)
        if (
            invitation is None
            or invitation.accepted_at is not None
            or invitation.expires_at < now
        ):
            return None
        if await self.authors.get_by_email(invitation.email) is not None:
            return None
        author = Author(
            email=invitation.email,
            display_name=display_name,
            role=Role.author,
            password_hash=hash_password(password),
        )
        await self.authors.add(author)
        invitation.accepted_at = now
        return author
