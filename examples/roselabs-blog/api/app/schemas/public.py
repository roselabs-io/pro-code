import datetime as dt

from pydantic import BaseModel

from app.schemas.comment import PublicComment


class PublicPostSummary(BaseModel):
    slug: str
    title: str
    excerpt: str
    published_at: dt.datetime | None
    author_name: str
    tags: list[str] = []


class PublicPostOut(PublicPostSummary):
    content_html: str
    comments: list[PublicComment] = []


class PublicListOut(BaseModel):
    items: list[PublicPostSummary]
    next_cursor: dt.datetime | None
