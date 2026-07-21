import datetime as dt
import uuid

from pydantic import BaseModel, ConfigDict

from app.models.comment import CommentStatus


class CommentCreate(BaseModel):
    author_name: str
    author_email: str
    body: str


class PublicComment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    author_name: str
    body: str
    created_at: dt.datetime


class ModerationComment(BaseModel):
    id: uuid.UUID
    post_slug: str
    post_title: str
    author_name: str
    author_email: str
    body: str
    status: CommentStatus
    created_at: dt.datetime
