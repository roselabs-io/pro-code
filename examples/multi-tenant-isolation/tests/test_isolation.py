"""The hard-done certification — no cross-tenant read, list, or write, ever.

A cross-tenant id must be indistinguishable from not-found (404, never 403). These tests
hit the real query path (no mocks) — the only way the isolation invariant is proven.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.auth import Role
from tests.conftest import auth, make_project


def test_cross_tenant_get_is_404(client: TestClient) -> None:
    b_project = make_project(client, "ws-b", name="Secret")
    resp = client.get(f"/projects/{b_project['id']}", headers=auth("ws-a"))
    assert resp.status_code == 404
    # The body must not leak that the row exists elsewhere.
    assert "Secret" not in resp.text
    assert b_project["id"] not in resp.text


def test_cross_tenant_id_matches_a_pure_miss(client: TestClient) -> None:
    b_project = make_project(client, "ws-b", name="Secret")
    cross = client.get(f"/projects/{b_project['id']}", headers=auth("ws-a"))
    missing = client.get("/projects/does-not-exist", headers=auth("ws-a"))
    assert cross.status_code == missing.status_code == 404
    assert cross.json() == missing.json()


def test_cross_tenant_patch_cannot_mutate(client: TestClient) -> None:
    b_project = make_project(client, "ws-b", name="Original")
    resp = client.patch(
        f"/projects/{b_project['id']}", json={"name": "Hacked"}, headers=auth("ws-a")
    )
    assert resp.status_code == 404
    still = client.get(f"/projects/{b_project['id']}", headers=auth("ws-b"))
    assert still.json()["name"] == "Original"


def test_cross_tenant_delete_cannot_remove(client: TestClient) -> None:
    b_project = make_project(client, "ws-b", name="Original")
    resp = client.delete(
        f"/projects/{b_project['id']}", headers=auth("ws-a", "admin", Role.ADMIN)
    )
    assert resp.status_code == 404
    still = client.get(f"/projects/{b_project['id']}", headers=auth("ws-b"))
    assert still.status_code == 200


def test_list_never_includes_another_tenant(client: TestClient) -> None:
    for i in range(5):
        make_project(client, "ws-b", name=f"B{i}")
    resp = client.get("/projects", headers=auth("ws-a"))
    assert resp.json()["items"] == []


def test_isolation_holds_across_every_verb(client: TestClient) -> None:
    """Certification: one foreign id, every verb, all 404 — the invariant, end to end."""
    b_project = make_project(client, "ws-b", name="Fort Knox")
    fid = b_project["id"]
    a_admin = auth("ws-a", "admin", Role.ADMIN)
    assert client.get(f"/projects/{fid}", headers=a_admin).status_code == 404
    assert (
        client.patch(f"/projects/{fid}", json={"name": "x"}, headers=a_admin).status_code
        == 404
    )
    assert client.delete(f"/projects/{fid}", headers=a_admin).status_code == 404
    # And ws-b still sees an untouched row.
    intact = client.get(f"/projects/{fid}", headers=auth("ws-b"))
    assert intact.status_code == 200
    assert intact.json()["name"] == "Fort Knox"
