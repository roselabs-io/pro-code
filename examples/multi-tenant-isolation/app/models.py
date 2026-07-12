"""Domain models — the Caller identity, the Project, and the request/response bodies."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.config import MAX_NAME_LEN, MIN_NAME_LEN


class Caller(BaseModel):
    """The resolved identity behind a request; the tenant boundary is workspace_id."""

    workspace_id: str
    role: str
    subject: str


class Project(BaseModel):
    """A unit of work owned by exactly one workspace."""

    id: str
    workspace_id: str
    name: str
    description: str = ""
    created_at: str


class ProjectCreate(BaseModel):
    """Create body — name is required and length-bounded; a bad body is a 422."""

    name: str = Field(min_length=MIN_NAME_LEN, max_length=MAX_NAME_LEN)
    description: str = ""


class ProjectUpdate(BaseModel):
    """Patch body — every field optional, but an all-empty patch is rejected upstream."""

    name: str | None = Field(
        default=None, min_length=MIN_NAME_LEN, max_length=MAX_NAME_LEN
    )
    description: str | None = None


class ProjectPage(BaseModel):
    """A cursor page — the stable next_cursor is null at the end of the list."""

    items: list[Project]
    next_cursor: str | None = None
