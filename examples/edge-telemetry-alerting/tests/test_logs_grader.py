"""Logs grader — the no-missed-critical promise proven from the trace, not the alert list.

A passing alert list could mask a wiring bug; the ``ALERT_RAISED{severity:critical}``
event is the independent proof the critical path fired.
"""

from __future__ import annotations

from collections.abc import Callable

from engine.log import ALERT_RAISED, LOG
from engine.monitor import Monitor
from engine.severity import Severity

CRITICAL = Severity.CRITICAL.value


def _critical_raised() -> list[dict]:
    return [r for r in LOG.with_code(ALERT_RAISED) if r["severity"] == CRITICAL]


def test_overpressure_emits_critical_alert_raised(
    run_fixture: Callable[..., Monitor],
) -> None:
    run_fixture("overpressure.jsonl")
    critical = _critical_raised()
    assert len(critical) == 1
    assert critical[0]["signal"] == "discharge_pressure"
    assert critical[0]["level"] == CRITICAL


def test_dead_from_boot_emits_critical_alert_raised(
    run_fixture: Callable[..., Monitor],
) -> None:
    run_fixture("dead_from_boot.jsonl")
    assert any(r["signal"] == "bearing_temperature" for r in _critical_raised())


def test_nominal_emits_no_alert(run_fixture: Callable[..., Monitor]) -> None:
    run_fixture("nominal.jsonl")
    assert LOG.with_code(ALERT_RAISED) == []
