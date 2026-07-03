"""Projects API — every route is workspace-scoped at the boundary.

Isolation is enforced here, at the request boundary: a route resolves the caller
(``get_caller``), then every store call carries ``caller.workspace_id``. A cross-tenant id
falls through to 404 (indistinguishable from not-found) and emits ``CROSS_TENANT_DENIED``.
"""

from __future__ import annotations

from fastapi import FastAPI, Query, Response

from app.auth import Caller, CallerDep, Role
from app.config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.errors import ApiError, Forbidden, NotFound, api_error_handler
from app.log import (
    CROSS_TENANT_DENIED,
    LOG,
    PROJECT_CREATED,
    PROJECT_DELETED,
    PROJECT_UPDATED,
    RBAC_DENIED,
)
from app.models import ProjectCreate, ProjectOut, ProjectPage, ProjectUpdate
from app.store import STORE, Project

app = FastAPI(title="Multi-tenant Projects API")
app.add_exception_handler(ApiError, api_error_handler)


def _serialize(project: Project) -> ProjectOut:
    return ProjectOut(
        id=project.id,
        workspace_id=project.workspace_id,
        name=project.name,
        description=project.description,
        created_by=project.created_by,
    )


def _load_own(caller: Caller, project_id: str) -> Project:
    project = STORE.get(caller.workspace_id, project_id)
    if project is None:
        LOG.event(
            CROSS_TENANT_DENIED,
            "warning",
            workspace=caller.workspace_id,
            target=project_id,
        )
        raise NotFound()
    return project


@app.post("/projects", response_model=ProjectOut, status_code=201)
def create_project(body: ProjectCreate, caller: CallerDep) -> ProjectOut:
    project = STORE.create(
        workspace_id=caller.workspace_id,
        name=body.name,
        description=body.description,
        created_by=caller.actor_id,
    )
    LOG.event(PROJECT_CREATED, "info", workspace=caller.workspace_id, id=project.id)
    return _serialize(project)


@app.get("/projects", response_model=ProjectPage)
def list_projects(
    caller: CallerDep,
    cursor: str | None = Query(default=None),
    limit: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
) -> ProjectPage:
    rows, next_cursor = STORE.list(caller.workspace_id, after=cursor, limit=limit)
    return ProjectPage(items=[_serialize(r) for r in rows], next_cursor=next_cursor)


@app.get("/projects/{project_id}", response_model=ProjectOut)
def get_project(project_id: str, caller: CallerDep) -> ProjectOut:
    return _serialize(_load_own(caller, project_id))


@app.patch("/projects/{project_id}", response_model=ProjectOut)
def update_project(project_id: str, body: ProjectUpdate, caller: CallerDep) -> ProjectOut:
    _load_own(caller, project_id)
    project = STORE.update(
        caller.workspace_id, project_id, name=body.name, description=body.description
    )
    assert project is not None
    LOG.event(PROJECT_UPDATED, "info", workspace=caller.workspace_id, id=project.id)
    return _serialize(project)


@app.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: str, caller: CallerDep) -> Response:
    project = _load_own(caller, project_id)
    if caller.role is not Role.ADMIN:
        LOG.event(
            RBAC_DENIED,
            "warning",
            workspace=caller.workspace_id,
            actor=caller.actor_id,
            target=project.id,
        )
        raise Forbidden("Only an admin may delete a project")
    STORE.delete(caller.workspace_id, project_id)
    LOG.event(PROJECT_DELETED, "info", workspace=caller.workspace_id, id=project_id)
    return Response(status_code=204)
