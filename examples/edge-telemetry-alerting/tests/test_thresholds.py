"""Threshold tiering — a value maps to the right severity at the boundaries."""

from __future__ import annotations

from engine.config import load_station
from engine.models import Reading
from engine.monitor import Monitor
from engine.severity import Severity


def _feed(values: list[float]) -> Monitor:
    """Feed discharge_pressure values (debounce 1) and return the monitor."""
    m = Monitor(load_station())
    for i, v in enumerate(values):
        m.process(Reading(signal="discharge_pressure", value=v, ts=1000.0 + i))
    return m


def test_below_warn_is_nominal() -> None:
    m = _feed([7.0])
    sev = next(s.severity for s in m.state_at(1000.5) if s.name == "discharge_pressure")
    assert sev == Severity.NOMINAL


def test_at_warn_is_warning() -> None:
    m = _feed([8.6])
    sev = next(s.severity for s in m.state_at(1000.5) if s.name == "discharge_pressure")
    assert sev == Severity.WARNING


def test_at_critical_is_critical() -> None:
    m = _feed([10.5])
    sev = next(s.severity for s in m.state_at(1000.5) if s.name == "discharge_pressure")
    assert sev == Severity.CRITICAL


def test_low_direction_rule_fires_a_warning() -> None:
    """The low-flow fixture drives the low-direction level rule to WARNING (fire case)."""
    from tests.conftest import raised, replay_fixture

    m = replay_fixture("low_flow")
    warnings = raised("warning")
    assert [e["signal"] for e in warnings] == ["flow_rate"]
    flow = next(s for s in m.state_at(1002.5) if s.name == "flow_rate")
    assert flow.severity == Severity.WARNING
