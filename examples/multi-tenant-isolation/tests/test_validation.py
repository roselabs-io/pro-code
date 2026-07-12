"""Severity-tiered validation — a blocking-invalid body is 422; no write lands."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.config import MAX_NAME_LEN
from tests.conftest import auth


def test_missing_name_is_422(client: TestClient) -> None:
    r = client.post("/projects", json={"description": "d"}, headers=auth("A"))
    assert r.status_code == 422


def test_empty_name_is_422(client: TestClient) -> None:
    r = client.post("/projects", json={"name": ""}, headers=auth("A"))
    assert r.status_code == 422


def test_overlong_name_is_422(client: TestClient) -> None:
    r = client.post(
        "/projects", json={"name": "x" * (MAX_NAME_LEN + 1)}, headers=auth("A")
    )
    assert r.status_code == 422


def test_empty_patch_is_422(client: TestClient) -> None:
    pid = client.post("/projects", json={"name": "a"}, headers=auth("A")).json()["id"]
    r = client.patch(f"/projects/{pid}", json={}, headers=auth("A"))
    assert r.status_code == 422
