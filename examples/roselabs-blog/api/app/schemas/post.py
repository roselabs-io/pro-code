import datetime as dt
import uuid

from pydantic import BaseModel, ConfigDict

from app.models.post import PostStatus


class PostCreate(BaseModel):
    title: str
    content_html: str
    excerpt: str = ""


class PostUpdate(BaseModel):
    title: str | None = None
    content_html: str | None = None
    excerpt: str | None = None


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    author_id: uuid.UUID
    title: str
    slug: str
    content_html: str
    excerpt: str
    status: PostStatus
    published_at: dt.datetime | None
    created_at: dt.datetime
