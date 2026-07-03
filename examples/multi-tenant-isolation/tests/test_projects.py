"""Integration test per endpoint — drive the real request, assert the effect."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.auth import Role
from tests.conftest import auth, make_project


def test_create_returns_row_scoped_to_workspace(client: TestClient) -> None:
    resp = client.post("/projects", json={"name": "Apollo"}, headers=auth("ws-a", "u1"))
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Apollo"
    assert body["workspace_id"] == "ws-a"
    assert body["created_by"] == "u1"
    assert body["id"]


def test_get_returns_the_created_row(client: TestClient) -> None:
    created = make_project(client, "ws-a", name="Apollo")
    resp = client.get(f"/projects/{created['id']}", headers=auth("ws-a"))
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_list_returns_only_this_workspace(client: TestClient) -> None:
    make_project(client, "ws-a", name="A1")
    make_project(client, "ws-a", name="A2")
    make_project(client, "ws-b", name="B1")
    resp = client.get("/projects", headers=auth("ws-a"))
    assert resp.status_code == 200
    names = {i["name"] for i in resp.json()["items"]}
    assert names == {"A1", "A2"}


def test_patch_mutates_the_row(client: TestClient) -> None:
    created = make_project(client, "ws-a", name="Old")
    resp = client.patch(
        f"/projects/{created['id']}", json={"name": "New"}, headers=auth("ws-a")
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "New"
    refetched = client.get(f"/projects/{created['id']}", headers=auth("ws-a"))
    assert refetched.json()["name"] == "New"


def test_delete_removes_the_row(client: TestClient) -> None:
    created = make_project(client, "ws-a", name="Doomed")
    resp = client.delete(
        f"/projects/{created['id']}", headers=auth("ws-a", "admin", Role.ADMIN)
    )
    assert resp.status_code == 204
    gone = client.get(f"/projects/{created['id']}", headers=auth("ws-a"))
    assert gone.status_code == 404


def test_description_defaults_and_serializes(client: TestClient) -> None:
    created = make_project(client, "ws-a", name="Apollo")
    assert created["description"] == ""
