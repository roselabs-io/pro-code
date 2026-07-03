"""Role gate at the boundary — only an admin deletes; isolation trumps the role check."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.auth import Role
from tests.conftest import auth, make_project


def test_member_cannot_delete(client: TestClient) -> None:
    created = make_project(client, "ws-a", name="P")
    resp = client.delete(
        f"/projects/{created['id']}", headers=auth("ws-a", "m", Role.MEMBER)
    )
    assert resp.status_code == 403
    assert resp.json()["code"] == "forbidden"
    # The row survives a denied delete.
    assert (
        client.get(f"/projects/{created['id']}", headers=auth("ws-a")).status_code == 200
    )


def test_admin_can_delete(client: TestClient) -> None:
    created = make_project(client, "ws-a", name="P")
    resp = client.delete(
        f"/projects/{created['id']}", headers=auth("ws-a", "a", Role.ADMIN)
    )
    assert resp.status_code == 204


def test_cross_tenant_hides_existence_even_from_admin(client: TestClient) -> None:
    """A foreign row is 404 (not 403) even to an admin — 403 would confirm it exists."""
    b_project = make_project(client, "ws-b", name="P")
    resp = client.delete(
        f"/projects/{b_project['id']}", headers=auth("ws-a", "a", Role.ADMIN)
    )
    assert resp.status_code == 404
