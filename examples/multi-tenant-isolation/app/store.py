"""In-memory project store — every read and write is workspace-scoped (deny by default).

The tenant-scoped-query-guard shape, made literal: no method reaches a row without a
``workspace_id`` argument, and a lookup for a row in another workspace returns ``None`` —
indistinguishable from a row that never existed. There is no unscoped accessor to misuse.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass
class Project:
    id: str
    workspace_id: str
    name: str
    description: str
    created_by: str


class ProjectStore:
    def __init__(self) -> None:
        self._rows: dict[str, Project] = {}

    def create(
        self, workspace_id: str, name: str, description: str, created_by: str
    ) -> Project:
        project = Project(
            id=uuid.uuid4().hex,
            workspace_id=workspace_id,
            name=name,
            description=description,
            created_by=created_by,
        )
        self._rows[project.id] = project
        return project

    def get(self, workspace_id: str, project_id: str) -> Project | None:
        row = self._rows.get(project_id)
        if row is None or row.workspace_id != workspace_id:
            return None
        return row

    def list(
        self, workspace_id: str, after: str | None, limit: int
    ) -> tuple[list[Project], str | None]:
        scoped = sorted(
            (r for r in self._rows.values() if r.workspace_id == workspace_id),
            key=lambda r: r.id,
        )
        start = 0
        if after is not None:
            start = next((i + 1 for i, r in enumerate(scoped) if r.id == after), 0)
        window = scoped[start : start + limit]
        next_cursor = window[-1].id if len(scoped) > start + limit else None
        return window, next_cursor

    def update(
        self,
        workspace_id: str,
        project_id: str,
        name: str | None,
        description: str | None,
    ) -> Project | None:
        row = self.get(workspace_id, project_id)
        if row is None:
            return None
        if name is not None:
            row.name = name
        if description is not None:
            row.description = description
        return row

    def delete(self, workspace_id: str, project_id: str) -> bool:
        row = self.get(workspace_id, project_id)
        if row is None:
            return False
        del self._rows[project_id]
        return True


STORE = ProjectStore()
