"""Cursor pagination — stable workspace-scoped pages ending in a null cursor."""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import auth


def _seed(client: TestClient, workspace: str, n: int) -> None:
    for i in range(n):
        client.post("/projects", json={"name": f"p{i}"}, headers=auth(workspace))


def test_pages_walk_the_whole_list_without_overlap(client: TestClient) -> None:
    _seed(client, "A", 5)
    seen: list[str] = []
    cursor = None
    for _ in range(10):  # bounded loop — must terminate well before this
        params = {"limit": 2}
        if cursor:
            params["cursor"] = cursor
        page = client.get("/projects", params=params, headers=auth("A")).json()
        seen.extend(p["name"] for p in page["items"])
        cursor = page["next_cursor"]
        if cursor is None:
            break
    assert seen == ["p0", "p1", "p2", "p3", "p4"]
    assert len(seen) == len(set(seen)), "no row appears on two pages"


def test_last_page_has_null_cursor(client: TestClient) -> None:
    _seed(client, "A", 2)
    page = client.get("/projects", params={"limit": 5}, headers=auth("A")).json()
    assert page["next_cursor"] is None
    assert len(page["items"]) == 2


def test_empty_workspace_lists_empty(client: TestClient) -> None:
    page = client.get("/projects", headers=auth("A")).json()
    assert page == {"items": [], "next_cursor": None}
