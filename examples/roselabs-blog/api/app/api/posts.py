import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_author
from app.core.db import get_session
from app.core.log import log_event
from app.models.author import Author
from app.models.post import Post
from app.schemas.post import PostCreate, PostOut, PostUpdate
from app.services.posts import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


def _post_out(post: Post) -> PostOut:
    return PostOut(
        id=post.id,
        author_id=post.author_id,
        title=post.title,
        slug=post.slug,
        content_html=post.content_html,
        excerpt=post.excerpt,
        status=post.status,
        published_at=post.published_at,
        created_at=post.created_at,
        tags=[tag.name for tag in post.tags],
    )


def _not_found(post_id: uuid.UUID, requester: uuid.UUID) -> HTTPException:
    log_event("POST_ACCESS_DENIED", post=str(post_id), requester=str(requester))
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(
    body: PostCreate,
    current: Author = Depends(get_current_author),
    session: AsyncSession = Depends(get_session),
) -> PostOut:
    return _post_out(await PostService(session).create_draft(current, body))


@router.get("/mine", response_model=list[PostOut])
async def list_my_posts(
    current: Author = Depends(get_current_author),
    session: AsyncSession = Depends(get_session),
) -> list[PostOut]:
    posts = await PostService(session).list_mine(current)
    return [_post_out(post) for post in posts]


@router.get("/{post_id}", response_model=PostOut)
async def get_post(
    post_id: uuid.UUID,
    current: Author = Depends(get_current_author),
    session: AsyncSession = Depends(get_session),
) -> PostOut:
    post = await PostService(session).get_owned(current, post_id)
    if post is None:
        raise _not_found(post_id, current.id)
    return _post_out(post)


@router.patch("/{post_id}", response_model=PostOut)
async def update_post(
    post_id: uuid.UUID,
    body: PostUpdate,
    current: Author = Depends(get_current_author),
    session: AsyncSession = Depends(get_session),
) -> PostOut:
    post = await PostService(session).update(current, post_id, body)
    if post is None:
        raise _not_found(post_id, current.id)
    return _post_out(post)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: uuid.UUID,
    current: Author = Depends(get_current_author),
    session: AsyncSession = Depends(get_session),
) -> None:
    deleted = await PostService(session).delete(current, post_id)
    if not deleted:
        raise _not_found(post_id, current.id)


@router.post("/{post_id}/publish", response_model=PostOut)
async def publish_post(
    post_id: uuid.UUID,
    current: Author = Depends(get_current_author),
    session: AsyncSession = Depends(get_session),
) -> PostOut:
    post = await PostService(session).set_status(current, post_id, publish=True)
    if post is None:
        raise _not_found(post_id, current.id)
    return _post_out(post)


@router.post("/{post_id}/unpublish", response_model=PostOut)
async def unpublish_post(
    post_id: uuid.UUID,
    current: Author = Depends(get_current_author),
    session: AsyncSession = Depends(get_session),
) -> PostOut:
    post = await PostService(session).set_status(current, post_id, publish=False)
    if post is None:
        raise _not_found(post_id, current.id)
    return _post_out(post)
