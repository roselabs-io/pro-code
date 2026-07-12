"""Staleness — a dropped sensor renders '— stale' and alerts by criticality."""

from __future__ import annotations

from engine.config import load_station
from engine.models import Reading
from engine.monitor import Monitor
from engine.severity import Severity


def _status(m: Monitor, name: str, now: float):
    return next(s for s in m.state_at(now) if s.name == name)


def test_fresh_signal_shows_its_value() -> None:
    m = Monitor(load_station())
    m.process(Reading(signal="bearing_temp", value=73.0, ts=1000.0))
    s = _status(m, "bearing_temp", 1005.0)  # within the 10s TTL
    assert s.stale is False
    assert s.value == 73.0
    assert s.label == "NOMINAL"


def test_past_ttl_is_stale_and_value_nulled() -> None:
    m = Monitor(load_station())
    m.process(Reading(signal="bearing_temp", value=73.0, ts=1000.0))
    s = _status(m, "bearing_temp", 1011.0)  # 11s > 10s TTL
    assert s.stale is True
    assert s.value is None, "the last-good number must NOT render when stale"
    assert s.label == "— stale"


def test_stale_safety_critical_is_critical() -> None:
    m = Monitor(load_station())
    m.process(Reading(signal="bearing_temp", value=73.0, ts=1000.0))
    s = _status(m, "bearing_temp", 1011.0)
    assert s.severity == Severity.CRITICAL


def test_dead_from_boot_is_stale_critical() -> None:
    """A never-reported safety-critical signal is stale-critical from boot, not blank."""
    m = Monitor(load_station())
    s = _status(m, "bearing_temp", 1.0)
    assert s.stale is True
    assert s.severity == Severity.CRITICAL
    assert s.value is None


def test_stale_non_safety_critical_is_warning() -> None:
    m = Monitor(load_station())
    m.process(Reading(signal="flow_rate", value=40.0, ts=1000.0))
    s = _status(m, "flow_rate", 1040.0)  # 40s > 30s TTL
    assert s.stale is True
    assert s.severity == Severity.WARNING


def test_reading_again_clears_staleness() -> None:
    m = Monitor(load_station())
    m.process(Reading(signal="bearing_temp", value=73.0, ts=1000.0))
    assert _status(m, "bearing_temp", 1011.0).stale is True
    m.process(Reading(signal="bearing_temp", value=74.0, ts=1012.0))
    fresh = _status(m, "bearing_temp", 1013.0)
    assert fresh.stale is False
    assert fresh.value == 74.0
