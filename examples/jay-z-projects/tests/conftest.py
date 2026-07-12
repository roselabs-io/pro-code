"""Test harness — a live signing key, freshly-minted tokens, a clean store each test."""

from __future__ import annotations

import jwt
import pytest
from fastapi.testclient import TestClient

from app import log
from app.config import JWT_ALGORITHM
from app.store import store

SECRET = "test-secret-not-a-real-key-padded-to-32-plus-bytes"


@pytest.fixture(autouse=True)
def _configured_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Every test runs with the key in the pocket; the fail-closed test pulls it."""
    monkeypatch.setenv("PROJECTS_JWT_SECRET", SECRET)


@pytest.fixture(autouse=True)
def _clean_state() -> None:
    """Clean store, clean trace each test — nobody inherits nobody's rows."""
    store._items.clear()
    log.reset()


@pytest.fixture
def client() -> TestClient:
    """A TestClient that hands you app errors as responses, not tracebacks."""
    return TestClient(app_())


def app_():
    from app.main import app

    return app


def token(workspace_id: str, role: str = "member", sub: str = "u1") -> str:
    """Mint a signed bearer token for a caller — their pass to get in."""
    return jwt.encode(
        {"workspace_id": workspace_id, "role": role, "sub": sub},
        SECRET,
        algorithm=JWT_ALGORITHM,
    )


def auth(workspace_id: str, role: str = "member", sub: str = "u1") -> dict[str, str]:
    """The Authorization header a caller shows at the door."""
    return {"Authorization": f"Bearer {token(workspace_id, role, sub)}"}
