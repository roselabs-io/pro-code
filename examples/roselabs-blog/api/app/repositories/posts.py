import datetime as dt
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.slug import slugify
from app.models.post import Post, PostStatus
from app.models.tag import Tag


class PostRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, post: Post) -> Post:
        self.session.add(post)
        await self.session.flush()
        await self.session.refresh(post)
        return post

    async def get(self, post_id: uuid.UUID) -> Post | None:
        return await self.session.get(Post, post_id)

    async def get_for_author(
        self, post_id: uuid.UUID, author_id: uuid.UUID
    ) -> Post | None:
        result = await self.session.execute(
            select(Post).where(Post.id == post_id, Post.author_id == author_id)
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Post | None:
        result = await self.session.execute(select(Post).where(Post.slug == slug))
        return result.scalar_one_or_none()

    async def list_for_author(self, author_id: uuid.UUID) -> list[Post]:
        result = await self.session.execute(
            select(Post)
            .where(Post.author_id == author_id)
            .order_by(Post.created_at.desc())
        )
        return list(result.scalars().all())

    async def delete(self, post: Post) -> None:
        await self.session.delete(post)

    async def get_by_slug_with_author(self, slug: str) -> Post | None:
        result = await self.session.execute(
            select(Post).options(selectinload(Post.author)).where(Post.slug == slug)
        )
        return result.scalar_one_or_none()

    async def list_published(
        self,
        limit: int,
        before: dt.datetime | None = None,
        tag: str | None = None,
    ) -> list[Post]:
        stmt = (
            select(Post)
            .options(selectinload(Post.author))
            .where(Post.status == PostStatus.published)
        )
        if tag is not None:
            stmt = stmt.join(Post.tags).where(Tag.slug == slugify(tag))
        if before is not None:
            stmt = stmt.where(Post.published_at < before)
        stmt = stmt.order_by(Post.published_at.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
