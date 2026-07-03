"""staleness-watchdog — missing data is an alert, never nominal (incl. dead-from-boot)."""

from __future__ import annotations

from collections.abc import Callable

from engine.models import AlertKind
from engine.monitor import Monitor
from engine.severity import Severity


def test_dropped_sensor_fires_critical(run_fixture: Callable[..., Monitor]) -> None:
    # discharge_pressure reports, then goes silent past its 5s TTL.
    monitor = run_fixture("stale_sensor.jsonl")
    alerts = monitor.active_alerts()
    assert len(alerts) == 1
    assert alerts[0].signal == "discharge_pressure"
    assert alerts[0].kind is AlertKind.STALENESS
    assert alerts[0].severity is Severity.CRITICAL


def test_dead_from_boot_sensor_fires_critical(
    run_fixture: Callable[..., Monitor],
) -> None:
    # bearing_temperature never reports at all; measured from station_start it is stale.
    monitor = run_fixture("dead_from_boot.jsonl")
    stale = [a for a in monitor.active_alerts() if a.kind is AlertKind.STALENESS]
    assert len(stale) == 1
    assert stale[0].signal == "bearing_temperature"
    assert stale[0].severity is Severity.CRITICAL


def test_nominal_stream_is_not_stale(run_fixture: Callable[..., Monitor]) -> None:
    monitor = run_fixture("nominal.jsonl")
    assert [a for a in monitor.active_alerts() if a.kind is AlertKind.STALENESS] == []


def test_fresh_reading_clears_staleness(run_fixture: Callable[..., Monitor]) -> None:
    monitor = run_fixture("stale_sensor.jsonl")
    assert monitor.active_alerts()  # stale now
    from engine.models import Reading

    monitor.process(Reading("discharge_pressure", 8.0, ts=100.0))
    assert monitor.active_alerts() == []  # a fresh reading ended the staleness
