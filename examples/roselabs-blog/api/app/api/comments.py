import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_author
from app.core.db import get_session
from app.core.log import log_event
from app.models.author import Author
from app.models.comment import Comment, CommentStatus
from app.schemas.comment import ModerationComment
from app.services.comments import CommentService

router = APIRouter(prefix="/comments", tags=["comments"])


def _moderation_view(comment: Comment) -> ModerationComment:
    return ModerationComment(
        id=comment.id,
        post_slug=comment.post.slug,
        post_title=comment.post.title,
        author_name=comment.author_name,
        author_email=comment.author_email,
        body=comment.body,
        status=comment.status,
        created_at=comment.created_at,
    )


def _not_found(comment_id: uuid.UUID, requester: uuid.UUID) -> HTTPException:
    log_event(
        "COMMENT_MODERATION_DENIED", comment=str(comment_id), requester=str(requester)
    )
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
    )


@router.get("/pending", response_model=list[ModerationComment])
async def list_pending(
    current: Author = Depends(get_current_author),
    session: AsyncSession = Depends(get_session),
) -> list[ModerationComment]:
    comments = await CommentService(session).list_pending_for(current)
    return [_moderation_view(c) for c in comments]


@router.post("/{comment_id}/approve", response_model=ModerationComment)
async def approve_comment(
    comment_id: uuid.UUID,
    current: Author = Depends(get_current_author),
    session: AsyncSession = Depends(get_session),
) -> ModerationComment:
    comment = await CommentService(session).moderate(
        current, comment_id, CommentStatus.approved
    )
    if comment is None:
        raise _not_found(comment_id, current.id)
    return _moderation_view(comment)


@router.post("/{comment_id}/hide", response_model=ModerationComment)
async def hide_comment(
    comment_id: uuid.UUID,
    current: Author = Depends(get_current_author),
    session: AsyncSession = Depends(get_session),
) -> ModerationComment:
    comment = await CommentService(session).moderate(
        current, comment_id, CommentStatus.hidden
    )
    if comment is None:
        raise _not_found(comment_id, current.id)
    return _moderation_view(comment)
