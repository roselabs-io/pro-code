"""Schema validation — pydantic rejects a malformed body with 422."""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import auth


def test_empty_name_is_422(client: TestClient) -> None:
    resp = client.post("/projects", json={"name": ""}, headers=auth("ws-a"))
    assert resp.status_code == 422


def test_missing_name_is_422(client: TestClient) -> None:
    resp = client.post("/projects", json={}, headers=auth("ws-a"))
    assert resp.status_code == 422


def test_over_page_limit_is_422(client: TestClient) -> None:
    resp = client.get("/projects", params={"limit": 10_000}, headers=auth("ws-a"))
    assert resp.status_code == 422
