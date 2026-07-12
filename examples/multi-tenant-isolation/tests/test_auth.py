"""Auth fails closed — a missing key, a missing token, or a bad token all deny."""

from __future__ import annotations

import jwt
import pytest
from fastapi.testclient import TestClient

from tests.conftest import SECRET, auth


def test_valid_token_resolves_caller(client: TestClient) -> None:
    r = client.get("/projects", headers=auth("A"))
    assert r.status_code == 200


def test_missing_token_is_401(client: TestClient) -> None:
    r = client.get("/projects")
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "unauthorized"


def test_bad_signature_is_401(client: TestClient) -> None:
    forged = jwt.encode(
        {"workspace_id": "A", "role": "member", "sub": "u1"},
        "a-different-wrong-key-also-padded-to-32-plus-bytes",
        algorithm="HS256",
    )
    r = client.get("/projects", headers={"Authorization": f"Bearer {forged}"})
    assert r.status_code == 401


def test_token_missing_claims_is_401(client: TestClient) -> None:
    thin = jwt.encode({"sub": "u1"}, SECRET, algorithm="HS256")
    r = client.get("/projects", headers={"Authorization": f"Bearer {thin}"})
    assert r.status_code == 401


def test_unconfigured_key_denies_no_dev_fallback(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """With no signing key configured, every request denies — no dev-open path."""
    monkeypatch.delenv("PROJECTS_JWT_SECRET", raising=False)
    r = client.get("/projects", headers=auth("A"))
    assert r.status_code == 401
