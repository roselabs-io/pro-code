"""Config + ingest — the station loads and a malformed line is rejected."""

from __future__ import annotations

import pytest

from engine.config import Station, load_station
from engine.replay import parse_line


def test_station_loads_signal_catalog(station: Station) -> None:
    names = [s.name for s in station.signals]
    assert names == ["bearing_temp", "discharge_pressure", "flow_rate"]


def test_safety_critical_signals_have_an_alert_condition(station: Station) -> None:
    """The hard-gate invariant: every safety-critical signal carries a rule + severity."""
    for spec in station.signals:
        if spec.safety_critical:
            assert spec.level is not None or spec.staleness is not None


def test_malformed_line_is_rejected() -> None:
    with pytest.raises(ValueError):
        parse_line('{"signal": "bearing_temp"}')  # missing value + ts
    with pytest.raises(ValueError):
        parse_line("not json at all")


def test_safety_critical_without_condition_fails_load(tmp_path) -> None:
    """A safety-critical signal with no alert condition fails loudly, not silently."""
    bad = tmp_path / "bad.toml"
    bad.write_text(
        'station = "x"\n[[signal]]\nname="s"\nunit="C"\nsafety_critical=true\n'
    )
    with pytest.raises(ValueError, match="no alert condition"):
        load_station(bad)


def test_valid_line_parses() -> None:
    reading = parse_line('{"signal": "bearing_temp", "value": 73.5, "ts": 1000.0}')
    assert reading.signal == "bearing_temp"
    assert reading.value == 73.5
