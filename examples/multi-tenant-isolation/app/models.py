"""Request/response schemas — pydantic validates the shape (a bad body → 422)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)


class ProjectOut(BaseModel):
    id: str
    workspace_id: str
    name: str
    description: str
    created_by: str


class ProjectPage(BaseModel):
    items: list[ProjectOut]
    next_cursor: str | None
