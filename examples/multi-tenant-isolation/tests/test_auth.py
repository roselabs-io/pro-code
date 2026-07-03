"""Auth at the boundary — no token, no access; a tampered token is rejected."""

from __future__ import annotations

import jwt
from fastapi.testclient import TestClient

from tests.conftest import auth


def test_missing_token_is_401(client: TestClient) -> None:
    resp = client.get("/projects")
    assert resp.status_code == 401
    assert resp.json()["code"] == "unauthorized"


def test_non_bearer_scheme_is_401(client: TestClient) -> None:
    resp = client.get("/projects", headers={"Authorization": "Basic abc"})
    assert resp.status_code == 401


def test_token_signed_with_wrong_secret_is_401(client: TestClient) -> None:
    forged = jwt.encode(
        {"ws": "ws-a", "sub": "u", "role": "admin"},
        "a-different-secret-of-adequate-length-000000",
        algorithm="HS256",
    )
    resp = client.get("/projects", headers={"Authorization": f"Bearer {forged}"})
    assert resp.status_code == 401


def test_valid_token_is_accepted(client: TestClient) -> None:
    resp = client.get("/projects", headers=auth("ws-a"))
    assert resp.status_code == 200
