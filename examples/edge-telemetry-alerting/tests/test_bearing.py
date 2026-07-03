"""bearing_temperature threshold rule — fire AND no-fire."""

from __future__ import annotations

from collections.abc import Callable

from engine.monitor import Monitor
from engine.severity import Severity


def test_bearing_overheat_fires_critical(run_fixture: Callable[..., Monitor]) -> None:
    monitor = run_fixture("bearing_overheat.jsonl")
    alerts = monitor.active_alerts()
    assert len(alerts) == 1
    assert alerts[0].signal == "bearing_temperature"
    assert alerts[0].severity is Severity.CRITICAL


def test_bearing_nominal_is_silent(run_fixture: Callable[..., Monitor]) -> None:
    monitor = run_fixture("nominal.jsonl")
    assert all(a.signal != "bearing_temperature" for a in monitor.active_alerts())
