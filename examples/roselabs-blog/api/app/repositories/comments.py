import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.comment import Comment, CommentStatus
from app.models.post import Post


class CommentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, comment: Comment) -> Comment:
        self.session.add(comment)
        await self.session.flush()
        await self.session.refresh(comment)
        return comment

    async def get_with_post(self, comment_id: uuid.UUID) -> Comment | None:
        result = await self.session.execute(
            select(Comment)
            .options(selectinload(Comment.post))
            .where(Comment.id == comment_id)
        )
        return result.scalar_one_or_none()

    async def list_approved(self, post_id: uuid.UUID) -> list[Comment]:
        result = await self.session.execute(
            select(Comment)
            .where(Comment.post_id == post_id, Comment.status == CommentStatus.approved)
            .order_by(Comment.created_at.asc())
        )
        return list(result.scalars().all())

    async def list_pending(self, author_id: uuid.UUID | None = None) -> list[Comment]:
        stmt = (
            select(Comment)
            .options(selectinload(Comment.post))
            .join(Post, Comment.post_id == Post.id)
            .where(Comment.status == CommentStatus.pending)
        )
        if author_id is not None:
            stmt = stmt.where(Post.author_id == author_id)
        stmt = stmt.order_by(Comment.created_at.asc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
