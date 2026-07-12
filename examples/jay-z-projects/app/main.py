"""Request boundary — pull a Caller, scope at the store, then check the role.

The order that carries weight is SCOPE before ROLE: a foreign id 404s before the role
check runs, so a 403 only ever shows for your own resource, never an existence tell.
"""

from __future__ import annotations

from fastapi import Depends, FastAPI, Query, Response

from app import log
from app.auth import ADMIN, get_caller
from app.config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE, MIN_PAGE_SIZE
from app.errors import ApiError, api_error_handler, forbidden, not_found
from app.models import Caller, Project, ProjectCreate, ProjectPage, ProjectUpdate
from app.store import store

app = FastAPI(title="jay-z-projects")
app.add_exception_handler(ApiError, api_error_handler)  # type: ignore[arg-type]


def _deny_cross_tenant(caller: Caller, project_id: str) -> ApiError:
    """Log the denial if the id belongs to another workspace, then 404 either way."""
    owner = store.owner_of(project_id)
    if owner is not None and owner != caller.workspace_id:
        log.emit(
            log.CROSS_TENANT_DENIED,
            level="warning",
            workspace=caller.workspace_id,
            target=project_id,
        )
    return not_found()


@app.get("/projects", response_model=ProjectPage)
def list_projects(
    caller: Caller = Depends(get_caller),
    cursor: str | None = Query(default=None),
    limit: int = Query(default=DEFAULT_PAGE_SIZE, ge=MIN_PAGE_SIZE, le=MAX_PAGE_SIZE),
) -> ProjectPage:
    """Hand back the caller's own-workspace projects, paged by cursor — nobody else's."""
    items, next_cursor = store.list(caller.workspace_id, cursor, limit)
    return ProjectPage(items=items, next_cursor=next_cursor)


@app.post("/projects", response_model=Project, status_code=201)
def create_project(body: ProjectCreate, caller: Caller = Depends(get_caller)) -> Project:
    """Stamp a new project with the caller's workspace and put it on the books."""
    project = store.create(caller.workspace_id, body.name, body.description)
    log.emit(log.PROJECT_CREATED, workspace=caller.workspace_id, id=project.id)
    return project


@app.get("/projects/{project_id}", response_model=Project)
def get_project(project_id: str, caller: Caller = Depends(get_caller)) -> Project:
    """Read one project that's yours; a foreign or missing id gets a flat 404."""
    project = store.get(caller.workspace_id, project_id)
    if project is None:
        raise _deny_cross_tenant(caller, project_id)
    return project


@app.patch("/projects/{project_id}", response_model=Project)
def update_project(
    project_id: str, body: ProjectUpdate, caller: Caller = Depends(get_caller)
) -> Project:
    """Patch a project that's yours — empty patch is 422, foreign or missing id is 404."""
    if body.name is None and body.description is None:
        raise ApiError(422, "empty_update", "at least one field must be provided")
    updated = store.update(caller.workspace_id, project_id, body.name, body.description)
    if updated is None:
        raise _deny_cross_tenant(caller, project_id)
    log.emit(log.PROJECT_UPDATED, workspace=caller.workspace_id, id=project_id)
    return updated


@app.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: str, caller: Caller = Depends(get_caller)) -> Response:
    """Cut a project that's yours — scope (404) checked BEFORE the admin gate (403)."""
    project = store.get(caller.workspace_id, project_id)
    if project is None:
        raise _deny_cross_tenant(caller, project_id)
    if caller.role != ADMIN:
        raise forbidden("delete requires the admin role")
    store.delete(caller.workspace_id, project_id)
    log.emit(log.PROJECT_DELETED, workspace=caller.workspace_id, id=project_id)
    return Response(status_code=204)
