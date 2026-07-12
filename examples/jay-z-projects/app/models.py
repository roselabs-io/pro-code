"""Domain models — the Caller, the Project, and the bodies that come and go."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.config import MAX_NAME_LEN, MIN_NAME_LEN


class Caller(BaseModel):
    """Who's behind the request — the whole tenant line rides on workspace_id."""

    workspace_id: str
    role: str
    subject: str


class Project(BaseModel):
    """A piece of work that answers to exactly one workspace."""

    id: str
    workspace_id: str
    name: str
    description: str = ""
    created_at: str


class ProjectCreate(BaseModel):
    """Create body — name's required and length-checked; a bad body catches a 422."""

    name: str = Field(min_length=MIN_NAME_LEN, max_length=MAX_NAME_LEN)
    description: str = ""


class ProjectUpdate(BaseModel):
    """Patch body — every field's optional, but an all-empty patch gets turned away."""

    name: str | None = Field(
        default=None, min_length=MIN_NAME_LEN, max_length=MAX_NAME_LEN
    )
    description: str | None = None


class ProjectPage(BaseModel):
    """A cursor page — next_cursor goes null when you hit the end of the list."""

    items: list[Project]
    next_cursor: str | None = None
