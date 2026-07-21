import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.models.post import Post
from app.schemas.comment import CommentCreate, PublicComment
from app.schemas.public import PublicListOut, PublicPostOut, PublicPostSummary
from app.services.comments import CommentService
from app.services.public import PublicService

router = APIRouter(prefix="/public", tags=["public"])


def _summary(post: Post) -> PublicPostSummary:
    return PublicPostSummary(
        slug=post.slug,
        title=post.title,
        excerpt=post.excerpt,
        published_at=post.published_at,
        author_name=post.author.display_name,
        tags=[tag.name for tag in post.tags],
    )


@router.get("/posts", response_model=PublicListOut)
async def list_published(
    limit: int = Query(10, ge=1, le=50),
    before: dt.datetime | None = None,
    tag: str | None = None,
    session: AsyncSession = Depends(get_session),
) -> PublicListOut:
    posts = await PublicService(session).list_published(limit, before, tag)
    items = [_summary(p) for p in posts]
    next_cursor = items[-1].published_at if len(items) == limit else None
    return PublicListOut(items=items, next_cursor=next_cursor)


@router.get("/posts/{slug}", response_model=PublicPostOut)
async def get_published(
    slug: str,
    session: AsyncSession = Depends(get_session),
) -> PublicPostOut:
    post = await PublicService(session).get_published(slug)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    comments = await CommentService(session).list_approved(post.id)
    return PublicPostOut(
        slug=post.slug,
        title=post.title,
        excerpt=post.excerpt,
        published_at=post.published_at,
        author_name=post.author.display_name,
        content_html=post.content_html,
        tags=[tag.name for tag in post.tags],
        comments=[PublicComment.model_validate(c) for c in comments],
    )


@router.post("/posts/{slug}/comments", status_code=status.HTTP_201_CREATED)
async def submit_comment(
    slug: str,
    body: CommentCreate,
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    post = await PublicService(session).get_published(slug)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    await CommentService(session).submit(post, body)
    return {"status": "pending"}
