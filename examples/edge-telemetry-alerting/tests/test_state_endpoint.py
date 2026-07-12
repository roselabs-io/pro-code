"""The /state contract — stale → null + '— stale', critical → critical."""

from __future__ import annotations

from fastapi.testclient import TestClient

from dashboard.app import app
from dashboard.seed import DEMO_NOW


def _client() -> TestClient:
    return TestClient(app)


def test_state_serializes_the_seed() -> None:
    body = _client().get("/state").json()
    assert body["station"] == "pump-house-1"
    by_name = {s["name"]: s for s in body["signals"]}
    assert set(by_name) == {"bearing_temp", "discharge_pressure", "flow_rate"}


def test_stale_signal_serializes_null_and_stale_label() -> None:
    """flow_rate reported at ts=900, read at DEMO_NOW=1012 → past its 30s TTL → stale."""
    body = _client().get("/state", params={"now": DEMO_NOW}).json()
    flow = next(s for s in body["signals"] if s["name"] == "flow_rate")
    assert flow["stale"] is True
    assert (
        flow["value"] is None
    ), "a stale value must serialize null, not the last-good number"
    assert flow["label"] == "— stale"


def test_critical_signal_serializes_critical() -> None:
    body = _client().get("/state", params={"now": DEMO_NOW}).json()
    pressure = next(s for s in body["signals"] if s["name"] == "discharge_pressure")
    assert pressure["severity"] == "critical"
    assert pressure["stale"] is False


def test_nominal_signal_serializes_its_value() -> None:
    body = _client().get("/state", params={"now": DEMO_NOW}).json()
    bearing = next(s for s in body["signals"] if s["name"] == "bearing_temp")
    assert bearing["severity"] == "nominal"
    assert bearing["value"] == 73.0
