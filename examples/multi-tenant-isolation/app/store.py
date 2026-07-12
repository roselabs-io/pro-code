"""Tenant-scoped project store — every query takes a workspace_id and denies by default.

Isolation lives HERE, at the data boundary: a foreign id resolves to None, never a row.
The handlers can't leak what the store won't hand them.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE, MIN_PAGE_SIZE
from app.models import Project


class ProjectStore:
    """In-memory projects, keyed by id, always accessed through a workspace scope."""

    def __init__(self) -> None:
        self._items: dict[str, Project] = {}

    def create(self, workspace_id: str, name: str, description: str) -> Project:
        """Write a project owned by this workspace."""
        pid = uuid.uuid4().hex
        project = Project(
            id=pid,
            workspace_id=workspace_id,
            name=name,
            description=description,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._items[pid] = project
        return project

    def get(self, workspace_id: str, project_id: str) -> Project | None:
        """Return the project if it's in this workspace, else None (deny-by-default)."""
        project = self._items.get(project_id)
        if project is None or project.workspace_id != workspace_id:
            return None
        return project

    def update(
        self,
        workspace_id: str,
        project_id: str,
        name: str | None,
        description: str | None,
    ) -> Project | None:
        """Patch a scoped project's mutable fields; None if it isn't in this workspace."""
        project = self.get(workspace_id, project_id)
        if project is None:
            return None
        updated = project.model_copy(
            update={
                "name": project.name if name is None else name,
                "description": project.description
                if description is None
                else description,
            }
        )
        self._items[project_id] = updated
        return updated

    def delete(self, workspace_id: str, project_id: str) -> bool:
        """Remove a scoped project; False if it isn't in this workspace."""
        if self.get(workspace_id, project_id) is None:
            return False
        del self._items[project_id]
        return True

    def owner_of(self, project_id: str) -> str | None:
        """The owning workspace of an id, for the audit trace only — never serialized."""
        project = self._items.get(project_id)
        return project.workspace_id if project else None

    def list(
        self, workspace_id: str, cursor: str | None, limit: int
    ) -> tuple[list[Project], str | None]:
        """Return this workspace's projects as a stable cursor page."""
        limit = max(MIN_PAGE_SIZE, min(limit, MAX_PAGE_SIZE))
        rows = [p for p in self._items.values() if p.workspace_id == workspace_id]
        start = 0
        if cursor is not None:
            ids = [p.id for p in rows]
            start = ids.index(cursor) + 1 if cursor in ids else len(rows)
        page = rows[start : start + limit]
        next_cursor = page[-1].id if start + limit < len(rows) and page else None
        return page, next_cursor


store = ProjectStore()

__all__ = ["ProjectStore", "store", "DEFAULT_PAGE_SIZE"]
