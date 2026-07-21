from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invitation import Invitation


class InvitationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, invitation: Invitation) -> Invitation:
        self.session.add(invitation)
        await self.session.flush()
        await self.session.refresh(invitation)
        return invitation

    async def get_by_token(self, token: str) -> Invitation | None:
        result = await self.session.execute(
            select(Invitation).where(Invitation.token == token)
        )
        return result.scalar_one_or_none()
