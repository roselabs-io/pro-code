"""threshold-with-hysteresis — a value flapping at the line is ONE alert, not N."""

from __future__ import annotations

from collections.abc import Callable

from engine.log import ALERT_RAISED, LOG
from engine.monitor import Monitor


def test_flapping_value_holds_one_alert(run_fixture: Callable[..., Monitor]) -> None:
    monitor = run_fixture("flap.jsonl")
    alerts = monitor.active_alerts()
    # Hysteresis holds the alert while the value hovers in the band; dedup keeps it one.
    assert len(alerts) == 1
    assert alerts[0].signal == "discharge_pressure"
    assert alerts[0].count > 1  # the sustained breach is counted, not re-raised


def test_flapping_raises_exactly_once(run_fixture: Callable[..., Monitor]) -> None:
    run_fixture("flap.jsonl")
    raised = [
        r for r in LOG.with_code(ALERT_RAISED) if r["signal"] == "discharge_pressure"
    ]
    assert len(raised) == 1
