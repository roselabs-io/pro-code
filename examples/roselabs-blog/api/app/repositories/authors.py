import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.author import Author


class AuthorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, author: Author) -> Author:
        self.session.add(author)
        await self.session.flush()
        return author

    async def get_by_email(self, email: str) -> Author | None:
        result = await self.session.execute(select(Author).where(Author.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, author_id: uuid.UUID) -> Author | None:
        return await self.session.get(Author, author_id)
