"""Debounce — a single-sample spike below the debounce count does not fire."""

from __future__ import annotations

from engine import log
from engine.config import load_station
from engine.models import Reading
from engine.monitor import Monitor


def test_single_spike_does_not_alert() -> None:
    """bearing_temp needs 2 consecutive breaches; one spike then recovery is silent."""
    m = Monitor(load_station())
    m.process(Reading(signal="bearing_temp", value=70.0, ts=1000.0))
    m.process(
        Reading(signal="bearing_temp", value=96.0, ts=1001.0)
    )  # one spike above crit
    m.process(
        Reading(signal="bearing_temp", value=71.0, ts=1002.0)
    )  # recovered next sample
    assert m.active_alerts() == []
    assert [e for e in log.events() if e["code"] == log.ALERT_RAISED] == []


def test_two_consecutive_breaches_do_fire() -> None:
    """Held for the debounce count → the alert fires (spike test isn't vacuous)."""
    m = Monitor(load_station())
    m.process(Reading(signal="bearing_temp", value=96.0, ts=1000.0))
    m.process(Reading(signal="bearing_temp", value=97.0, ts=1001.0))
    assert len(m.active_alerts()) == 1
