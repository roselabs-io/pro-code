"""RBAC at the boundary — delete's admin-only inside a tenant, gated after scope."""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import auth


def test_admin_can_delete_own(client: TestClient) -> None:
    pid = client.post("/projects", json={"name": "a"}, headers=auth("A", "admin")).json()[
        "id"
    ]
    assert (
        client.delete(f"/projects/{pid}", headers=auth("A", "admin")).status_code == 204
    )


def test_member_cannot_delete_own_is_403(client: TestClient) -> None:
    """A member swinging at an in-tenant delete catches a 403 — role gate after scope."""
    pid = client.post(
        "/projects", json={"name": "a"}, headers=auth("A", "member")
    ).json()["id"]
    r = client.delete(f"/projects/{pid}", headers=auth("A", "member"))
    assert r.status_code == 403
    assert r.json()["error"]["code"] == "forbidden"
    # The project walks away from the denied delete untouched.
    assert client.get(f"/projects/{pid}", headers=auth("A")).status_code == 200


def test_member_can_create_and_update(client: TestClient) -> None:
    pid = client.post(
        "/projects", json={"name": "a"}, headers=auth("A", "member")
    ).json()["id"]
    assert (
        client.patch(
            f"/projects/{pid}", json={"name": "b"}, headers=auth("A")
        ).status_code
        == 200
    )
