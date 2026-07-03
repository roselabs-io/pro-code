"""/state read model — the server serializes stale as null+flag (the browser honours it).

Proves the *server* side of the visual invariant: a stale signal serializes ``value: null,
stale: true``. (That the *client* renders it as "— stale" is the browser grader's job.)
"""

from __future__ import annotations

import time

from fastapi.testclient import TestClient

from dashboard.app import app, monitor
from dashboard.seed import seed_browser


def _seeded_client() -> TestClient:
    monitor.reset()
    seed_browser(monitor)
    return TestClient(app)


def test_stale_signal_serializes_null_and_flag() -> None:
    client = _seeded_client()
    state = client.get("/state").json()
    bearing = next(s for s in state["signals"] if s["name"] == "bearing_temperature")
    assert bearing["stale"] is True
    assert bearing["value"] is None  # a falsy field that MUST be present, not dropped
    assert bearing["status"] == "critical"


def test_critical_breach_serializes_value_and_status() -> None:
    client = _seeded_client()
    state = client.get("/state").json()
    pressure = next(s for s in state["signals"] if s["name"] == "discharge_pressure")
    assert pressure["stale"] is False
    assert pressure["value"] is not None
    assert pressure["status"] == "critical"


def test_ingest_updates_state() -> None:
    monitor.reset()
    client = TestClient(app)
    now = time.time()
    for i in range(3):
        resp = client.post(
            "/ingest",
            json={"signal": "discharge_pressure", "value": 11.0, "ts": now + i},
        )
        assert resp.status_code == 202
    state = client.get("/state").json()
    pressure = next(s for s in state["signals"] if s["name"] == "discharge_pressure")
    assert pressure["status"] == "critical"
