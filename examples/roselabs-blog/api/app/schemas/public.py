import datetime as dt

from pydantic import BaseModel


class PublicPostSummary(BaseModel):
    slug: str
    title: str
    excerpt: str
    published_at: dt.datetime | None
    author_name: str


class PublicPostOut(PublicPostSummary):
    content_html: str


class PublicListOut(BaseModel):
    items: list[PublicPostSummary]
    next_cursor: dt.datetime | None
