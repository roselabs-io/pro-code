import datetime as dt
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.slug import slugify
from app.models.author import Author, Role
from app.models.post import Post, PostStatus
from app.repositories.posts import PostRepository
from app.repositories.tags import TagRepository
from app.schemas.post import PostCreate, PostUpdate


class PostService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = PostRepository(session)
        self.tags = TagRepository(session)

    async def _unique_slug(self, title: str) -> str:
        base = slugify(title)
        candidate = base
        suffix = 2
        while await self.repo.get_by_slug(candidate) is not None:
            candidate = f"{base}-{suffix}"
            suffix += 1
        return candidate

    async def create_draft(self, author: Author, data: PostCreate) -> Post:
        post = Post(
            author_id=author.id,
            title=data.title,
            slug=await self._unique_slug(data.title),
            content_html=data.content_html,
            excerpt=data.excerpt,
            status=PostStatus.draft,
        )
        post.tags = await self.tags.get_or_create_many(data.tags)
        return await self.repo.add(post)

    async def list_mine(self, author: Author) -> list[Post]:
        return await self.repo.list_for_author(author.id)

    async def get_owned(self, actor: Author, post_id: uuid.UUID) -> Post | None:
        if actor.role is Role.admin:
            return await self.repo.get(post_id)
        return await self.repo.get_for_author(post_id, actor.id)

    async def update(
        self, actor: Author, post_id: uuid.UUID, data: PostUpdate
    ) -> Post | None:
        post = await self.get_owned(actor, post_id)
        if post is None:
            return None
        if data.title is not None:
            post.title = data.title
        if data.content_html is not None:
            post.content_html = data.content_html
        if data.excerpt is not None:
            post.excerpt = data.excerpt
        if data.tags is not None:
            post.tags = await self.tags.get_or_create_many(data.tags)
        return post

    async def delete(self, actor: Author, post_id: uuid.UUID) -> bool:
        post = await self.get_owned(actor, post_id)
        if post is None:
            return False
        await self.repo.delete(post)
        return True

    async def set_status(
        self, actor: Author, post_id: uuid.UUID, *, publish: bool
    ) -> Post | None:
        post = await self.get_owned(actor, post_id)
        if post is None:
            return None
        if publish:
            post.status = PostStatus.published
            if post.published_at is None:
                post.published_at = dt.datetime.now(dt.timezone.utc)
        else:
            post.status = PostStatus.draft
        return post
