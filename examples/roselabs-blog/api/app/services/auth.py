from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.models.author import Author
from app.repositories.authors import AuthorRepository


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = AuthorRepository(session)

    async def authenticate(self, email: str, password: str) -> Author | None:
        author = await self.repo.get_by_email(email)
        if author is None:
            return None
        if not verify_password(author.password_hash, password):
            return None
        return author
