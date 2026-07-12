"""Logs grader — the no-missed-critical promise proven from the TRACE, not the alert list.

A breach fixture must leave an ALERT_RAISED{severity:critical} event; the nominal fixture
must leave none.
"""

from __future__ import annotations

from engine import log
from tests.conftest import replay_fixture


def test_breach_emits_critical_event() -> None:
    replay_fixture("overpressure")
    crit = [
        e
        for e in log.events()
        if e["code"] == log.ALERT_RAISED and e["severity"] == "critical"
    ]
    assert crit, "the critical alert must be provable from the log trace"
    assert crit[0]["signal"] == "discharge_pressure"


def test_clear_emits_cleared_event() -> None:
    from engine.config import load_station
    from engine.models import Reading
    from engine.monitor import Monitor

    m = Monitor(load_station())
    m.process(Reading(signal="discharge_pressure", value=11.0, ts=1000.0))
    m.process(Reading(signal="discharge_pressure", value=7.0, ts=1001.0))
    assert any(e["code"] == log.ALERT_CLEARED for e in log.events())


def test_nominal_emits_no_alert_event() -> None:
    m = replay_fixture("nominal")
    m.state_at(1003.0)
    assert [e for e in log.events() if e["code"] == log.ALERT_RAISED] == []
