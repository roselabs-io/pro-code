"""Logs grader — prove behaviour from the trace, not the return value.

A 404 alone doesn't prove the isolation branch ran (a typo'd route also 404s). The
``CROSS_TENANT_DENIED`` event is what proves the scoped-query guard actually fired.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.auth import Role
from app.log import (
    CROSS_TENANT_DENIED,
    LOG,
    PROJECT_CREATED,
    RBAC_DENIED,
)
from tests.conftest import auth, make_project


def test_create_emits_project_created(client: TestClient) -> None:
    project = make_project(client, "ws-a", name="P")
    events = LOG.with_code(PROJECT_CREATED)
    assert len(events) == 1
    assert events[0]["workspace"] == "ws-a"
    assert events[0]["id"] == project["id"]


def test_cross_tenant_attempt_emits_denied_event(client: TestClient) -> None:
    b_project = make_project(client, "ws-b", name="Secret")
    LOG.clear()
    client.get(f"/projects/{b_project['id']}", headers=auth("ws-a"))
    denied = LOG.with_code(CROSS_TENANT_DENIED)
    assert len(denied) == 1
    assert denied[0]["level"] == "warning"
    assert denied[0]["workspace"] == "ws-a"
    assert denied[0]["target"] == b_project["id"]


def test_denied_delete_emits_rbac_event(client: TestClient) -> None:
    created = make_project(client, "ws-a", name="P")
    LOG.clear()
    client.delete(f"/projects/{created['id']}", headers=auth("ws-a", "m", Role.MEMBER))
    assert len(LOG.with_code(RBAC_DENIED)) == 1
