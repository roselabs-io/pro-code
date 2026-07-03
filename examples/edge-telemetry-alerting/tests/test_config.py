"""config-driven-thresholds — every safety-critical signal has a condition + severity."""

from __future__ import annotations

from engine.config import load_station
from engine.severity import Severity


def test_config_loads_from_toml() -> None:
    station = load_station()
    assert station.name == "Pump Station 7"
    assert set(station.signals) == {
        "discharge_pressure",
        "bearing_temperature",
        "flow_rate",
    }


def test_every_safety_critical_signal_has_a_rule() -> None:
    # The domain hard gate, checked in code: a safety-critical signal with no alert
    # condition/severity would be a silent hole.
    station = load_station()
    for name in station.safety_critical_signals():
        rule = station.signals[name]
        assert rule.limit is not None
        assert rule.staleness_ttl > 0
        assert rule.severity is Severity.CRITICAL


def test_severity_maps_to_the_enum() -> None:
    station = load_station()
    assert station.signals["flow_rate"].severity is Severity.WARNING
