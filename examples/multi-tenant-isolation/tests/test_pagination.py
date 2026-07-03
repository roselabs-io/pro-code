"""Cursor pagination — an unbounded list pages with a stable opaque cursor."""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import auth, make_project


def test_cursor_walks_every_row_once(client: TestClient) -> None:
    for i in range(5):
        make_project(client, "ws-a", name=f"P{i}")

    seen: list[str] = []
    cursor = None
    for _ in range(10):  # generous bound; loop exits on exhausted cursor
        params = {"limit": 2}
        if cursor:
            params["cursor"] = cursor
        page = client.get("/projects", params=params, headers=auth("ws-a")).json()
        seen.extend(i["id"] for i in page["items"])
        cursor = page["next_cursor"]
        if cursor is None:
            break

    assert len(seen) == 5
    assert len(set(seen)) == 5


def test_page_respects_limit(client: TestClient) -> None:
    for i in range(3):
        make_project(client, "ws-a", name=f"P{i}")
    page = client.get("/projects", params={"limit": 2}, headers=auth("ws-a")).json()
    assert len(page["items"]) == 2
    assert page["next_cursor"] is not None
