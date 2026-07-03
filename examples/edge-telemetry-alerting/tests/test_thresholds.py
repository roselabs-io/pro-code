"""discharge_pressure threshold rule — fixture-replay, fire AND no-fire."""

from __future__ import annotations

from collections.abc import Callable

from engine.models import AlertKind
from engine.monitor import Monitor
from engine.severity import Severity


def test_overpressure_fires_one_critical(run_fixture: Callable[..., Monitor]) -> None:
    monitor = run_fixture("overpressure.jsonl")
    alerts = monitor.active_alerts()
    assert len(alerts) == 1
    alert = alerts[0]
    assert alert.signal == "discharge_pressure"
    assert alert.severity is Severity.CRITICAL
    assert alert.kind is AlertKind.THRESHOLD
    # Debounce = 3: the breach at ts=1,2,3 fires on the third sample (ts=3), not before.
    assert alert.opened_at == 3.0


def test_nominal_pressure_is_silent(run_fixture: Callable[..., Monitor]) -> None:
    monitor = run_fixture("nominal.jsonl")
    assert monitor.active_alerts() == []
