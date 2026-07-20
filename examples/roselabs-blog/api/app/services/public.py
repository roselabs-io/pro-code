import datetime as dt

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.log import log_event
from app.models.post import Post, PostStatus
from app.repositories.posts import PostRepository


class PublicService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = PostRepository(session)

    async def list_published(self, limit: int, before: dt.datetime | None) -> list[Post]:
        return await self.repo.list_published(limit, before)

    async def get_published(self, slug: str) -> Post | None:
        post = await self.repo.get_by_slug_with_author(slug)
        if post is None:
            return None
        if post.status is not PostStatus.published:
            log_event("DRAFT_ACCESS_DENIED", post=slug, requester="anonymous")
            return None
        return post
