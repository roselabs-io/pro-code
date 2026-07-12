"""The core promise — no cross-tenant leak on ANY verb; no existence tell.

Every assertion drives the real request and checks the effect, not just the status.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import auth


def _b_project(client: TestClient) -> str:
    """Stand up a project owned by workspace B and hand back its id."""
    r = client.post("/projects", json={"name": "b-secret"}, headers=auth("B", "admin"))
    assert r.status_code == 201
    return r.json()["id"]


def test_cross_tenant_get_is_404_and_no_row_serializes(client: TestClient) -> None:
    bid = _b_project(client)
    r = client.get(f"/projects/{bid}", headers=auth("A"))
    assert r.status_code == 404
    assert "b-secret" not in r.text
    assert bid not in r.json().get("error", {}).get("detail", "")


def test_cross_tenant_patch_is_404(client: TestClient) -> None:
    bid = _b_project(client)
    r = client.patch(
        f"/projects/{bid}", json={"name": "hijacked"}, headers=auth("A", "admin")
    )
    assert r.status_code == 404
    # B's project ain't been touched.
    r2 = client.get(f"/projects/{bid}", headers=auth("B"))
    assert r2.json()["name"] == "b-secret"


def test_cross_tenant_delete_is_404(client: TestClient) -> None:
    bid = _b_project(client)
    r = client.delete(f"/projects/{bid}", headers=auth("A", "admin"))
    assert r.status_code == 404
    # B's project's still standing.
    assert client.get(f"/projects/{bid}", headers=auth("B")).status_code == 200


def test_member_cross_tenant_delete_is_404_not_403(client: TestClient) -> None:
    """Existence-oracle trap: scope checked BEFORE role, so a member catches a 404."""
    bid = _b_project(client)
    r = client.delete(f"/projects/{bid}", headers=auth("A", "member"))
    assert r.status_code == 404, "a 403 here would confirm B's id exists — the oracle"


def test_list_never_includes_another_workspace(client: TestClient) -> None:
    _b_project(client)
    client.post("/projects", json={"name": "a-own"}, headers=auth("A"))
    r = client.get("/projects", headers=auth("A"))
    names = [p["name"] for p in r.json()["items"]]
    assert names == ["a-own"]
    assert "b-secret" not in r.text
