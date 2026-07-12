"""Hysteresis — a value oscillating at the line holds ONE alert, not N or zero."""

from __future__ import annotations

from engine import log
from tests.conftest import replay_fixture


def test_oscillation_yields_exactly_one_active_alert() -> None:
    m = replay_fixture("flap")
    assert (
        len(m.active_alerts()) == 1
    ), "hysteresis holds one alert across the oscillation"


def test_oscillation_never_clears() -> None:
    """Without hysteresis, a dip below the line would clear then re-raise."""
    replay_fixture("flap")
    cleared = [e for e in log.events() if e["code"] == log.ALERT_CLEARED]
    raised = [e for e in log.events() if e["code"] == log.ALERT_RAISED]
    assert cleared == []
    assert len(raised) == 1, "one raise, no flap of raise/clear pairs"
