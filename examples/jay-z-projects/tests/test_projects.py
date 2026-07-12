"""CRUD integration tests — one per endpoint, we check the effect, not just talk."""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import auth


def test_create_returns_owned_project(client: TestClient) -> None:
    r = client.post(
        "/projects", json={"name": "alpha", "description": "d"}, headers=auth("A")
    )
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == "alpha"
    assert body["workspace_id"] == "A"
    assert body["description"] == "d"


def test_get_reads_own_project(client: TestClient) -> None:
    pid = client.post("/projects", json={"name": "alpha"}, headers=auth("A")).json()["id"]
    r = client.get(f"/projects/{pid}", headers=auth("A"))
    assert r.status_code == 200
    assert r.json()["id"] == pid


def test_get_missing_is_404(client: TestClient) -> None:
    r = client.get("/projects/does-not-exist", headers=auth("A"))
    assert r.status_code == 404


def test_update_changes_the_field(client: TestClient) -> None:
    pid = client.post("/projects", json={"name": "alpha"}, headers=auth("A")).json()["id"]
    r = client.patch(f"/projects/{pid}", json={"name": "renamed"}, headers=auth("A"))
    assert r.status_code == 200
    assert r.json()["name"] == "renamed"
    assert client.get(f"/projects/{pid}", headers=auth("A")).json()["name"] == "renamed"


def test_delete_removes_the_project(client: TestClient) -> None:
    pid = client.post("/projects", json={"name": "alpha"}, headers=auth("A")).json()["id"]
    r = client.delete(f"/projects/{pid}", headers=auth("A", "admin"))
    assert r.status_code == 204
    assert client.get(f"/projects/{pid}", headers=auth("A")).status_code == 404


def test_description_defaults_and_serializes(client: TestClient) -> None:
    """A falsy field (empty description) still shows up — it don't quietly vanish."""
    r = client.post("/projects", json={"name": "alpha"}, headers=auth("A"))
    assert "description" in r.json()
    assert r.json()["description"] == ""
