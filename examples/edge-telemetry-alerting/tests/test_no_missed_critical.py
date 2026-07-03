"""The hard-done certification — no missed critical alert.

Every real safety-critical breach (a bad value held, or a stale/dead-from-boot sensor)
raises a CRITICAL alert; a nominal stream stays silent. The analogue of the isolation
test in generic-saas: the grader, not confidence, certifies the core promise.
"""

from __future__ import annotations

from collections.abc import Callable

import pytest

from engine.log import ALERT_RAISED, LOG
from engine.monitor import Monitor
from engine.severity import Severity

# Each safety-critical failure mode → its fixture. Held bad value, dropped sensor,
# and dead-from-boot are all real breaches that MUST alert critical.
CRITICAL_FIXTURES = [
    "overpressure.jsonl",  # a bad pressure value, held past debounce
    "bearing_overheat.jsonl",  # a bad temperature value, held
    "stale_sensor.jsonl",  # a safety sensor that dropped out
    "dead_from_boot.jsonl",  # a safety sensor dead from boot (never reported)
]


@pytest.mark.parametrize("fixture", CRITICAL_FIXTURES)
def test_real_breach_raises_critical(
    fixture: str, run_fixture: Callable[..., Monitor]
) -> None:
    monitor = run_fixture(fixture)
    # Proven two independent ways: the active-alert list AND the emitted trace.
    critical_active = [
        a for a in monitor.active_alerts() if a.severity is Severity.CRITICAL
    ]
    critical_logged = [
        r for r in LOG.with_code(ALERT_RAISED) if r["severity"] == Severity.CRITICAL.value
    ]
    assert critical_active, f"{fixture}: no CRITICAL alert active — a missed critical"
    assert critical_logged, f"{fixture}: no ALERT_RAISED critical in the trace"


def test_nominal_stream_raises_nothing(run_fixture: Callable[..., Monitor]) -> None:
    monitor = run_fixture("nominal.jsonl")
    assert monitor.active_alerts() == []
    assert LOG.with_code(ALERT_RAISED) == []
