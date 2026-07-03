from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.auth import Role, issue_token
from app.log import LOG
from app.main import app
from app.store import STORE


@pytest.fixture(autouse=True)
def _reset_state() -> None:
    STORE._rows.clear()
    LOG.clear()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def auth(
    workspace: str, actor: str = "user-1", role: Role = Role.MEMBER
) -> dict[str, str]:
    return {"Authorization": f"Bearer {issue_token(workspace, actor, role)}"}


def make_project(
    client: TestClient, workspace: str, name: str = "P", **kw: object
) -> dict:
    headers = kw.pop("headers", None) or auth(workspace)
    resp = client.post("/projects", json={"name": name}, headers=headers)
    assert resp.status_code == 201, resp.text
    return resp.json()
