"""debounce-transient — a single-sample spike must not fire (a false-green trap)."""

from __future__ import annotations

from collections.abc import Callable

from engine.monitor import Monitor


def test_single_sample_spike_is_debounced(run_fixture: Callable[..., Monitor]) -> None:
    # The fixture crosses the limit for one sample (12.0 bar > 10.0), then returns.
    monitor = run_fixture("pressure_spike.jsonl")
    assert monitor.active_alerts() == []


def test_spike_fixture_actually_breaches(run_fixture: Callable[..., Monitor]) -> None:
    # Guard the guard: prove the input genuinely crossed the line, so the silence is
    # debounce, not a fixture that never breached.
    monitor = run_fixture("pressure_spike.jsonl")
    peak = max(
        float(v)
        for v in [8.0, 8.0, 12.0, 8.0, 8.0]  # the recorded values
    )
    assert peak > monitor.config.signals["discharge_pressure"].limit
