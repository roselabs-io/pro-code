"""The core promise — no missed critical alert.

Each fire fixture proves the critical path from the TRACE (ALERT_RAISED critical),
not just the active-alert list; the nominal fixture proves the rule stays quiet.
"""

from __future__ import annotations

from engine import log
from engine.severity import Severity
from tests.conftest import raised, replay_fixture


def test_bearing_overheat_raises_critical() -> None:
    m = replay_fixture("bearing_overheat")
    assert raised("critical"), "a bearing overheat must raise a CRITICAL alert"
    assert any(a.severity == Severity.CRITICAL for a in m.active_alerts())


def test_overpressure_raises_critical() -> None:
    m = replay_fixture("overpressure")
    crit = raised("critical")
    assert [e["signal"] for e in crit] == ["discharge_pressure"]
    assert any(a.severity == Severity.CRITICAL for a in m.active_alerts())


def test_dead_from_boot_raises_critical_on_read() -> None:
    """A never-reported safety-critical signal is CRITICAL from boot, seen on read."""
    m = replay_fixture("dead_from_boot")
    assert not raised("critical"), "nothing critical before the state is read"
    m.state_at(1001.0)
    crit = raised("critical")
    assert [e["signal"] for e in crit] == ["bearing_temp"]


def test_oscillating_breach_still_raises_critical() -> None:
    """A value oscillating in breach must not be debounced away into silence."""
    from engine.config import load_station
    from engine.models import Reading
    from engine.monitor import Monitor

    m = Monitor(load_station())
    # bearing_temp flips crit(96)/warn(90) — never nominal, repeatedly over crit 95.
    for i, v in enumerate([96.0, 90.0, 96.0, 90.0, 96.0]):
        m.process(Reading(signal="bearing_temp", value=v, ts=1000.0 + i))
    assert raised("critical"), "a sustained oscillating breach must still raise CRITICAL"


def test_nominal_fixture_raises_nothing() -> None:
    """The no-fire case — in-range data, read within TTL, is silent."""
    m = replay_fixture("nominal")
    m.state_at(1003.0)
    assert log.events() == []
    assert m.active_alerts() == []
