"""Logs grader — isolation proven from the TRACE, not the 404 alone.

A 404 could come from a genuinely-missing id; the CROSS_TENANT_DENIED event proves the
denial path actually fired against a real foreign resource.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app import log
from tests.conftest import auth


def test_cross_tenant_attempt_emits_denial_event(client: TestClient) -> None:
    bid = client.post("/projects", json={"name": "b"}, headers=auth("B", "admin")).json()[
        "id"
    ]
    log.reset()
    client.get(f"/projects/{bid}", headers=auth("A"))

    denials = [e for e in log.events() if e["code"] == log.CROSS_TENANT_DENIED]
    assert len(denials) == 1
    assert denials[0]["workspace"] == "A"
    assert denials[0]["target"] == bid
    assert denials[0]["level"] == "warning"


def test_genuine_miss_does_not_emit_denial(client: TestClient) -> None:
    """A truly-missing id is 404 but NOT a cross-tenant denial — event is specific."""
    log.reset()
    client.get("/projects/nope", headers=auth("A"))
    assert [e for e in log.events() if e["code"] == log.CROSS_TENANT_DENIED] == []


def test_create_emits_handler_ran_event(client: TestClient) -> None:
    log.reset()
    client.post("/projects", json={"name": "a"}, headers=auth("A"))
    created = [e for e in log.events() if e["code"] == log.PROJECT_CREATED]
    assert len(created) == 1
    assert created[0]["workspace"] == "A"
