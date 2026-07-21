import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.author import Author, Role
from app.models.comment import Comment, CommentStatus
from app.models.post import Post
from app.repositories.comments import CommentRepository
from app.schemas.comment import CommentCreate


class CommentService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = CommentRepository(session)

    async def submit(self, post: Post, data: CommentCreate) -> Comment:
        comment = Comment(
            post_id=post.id,
            author_name=data.author_name,
            author_email=data.author_email,
            body=data.body,
            status=CommentStatus.pending,
        )
        return await self.repo.add(comment)

    async def list_approved(self, post_id: uuid.UUID) -> list[Comment]:
        return await self.repo.list_approved(post_id)

    async def list_pending_for(self, actor: Author) -> list[Comment]:
        if actor.role is Role.admin:
            return await self.repo.list_pending(None)
        return await self.repo.list_pending(actor.id)

    async def moderate(
        self, actor: Author, comment_id: uuid.UUID, new_status: CommentStatus
    ) -> Comment | None:
        comment = await self.repo.get_with_post(comment_id)
        if comment is None:
            return None
        if actor.role is not Role.admin and comment.post.author_id != actor.id:
            return None
        comment.status = new_status
        return comment
