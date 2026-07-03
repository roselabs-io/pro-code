"""alert-dedup-storm-guard + out-of-order tolerance."""

from __future__ import annotations

from collections.abc import Callable

from engine.log import ALERT_RAISED, LOG
from engine.monitor import Monitor


def test_sustained_breach_is_one_alert_with_count(
    run_fixture: Callable[..., Monitor],
) -> None:
    monitor = run_fixture("overpressure.jsonl")
    alerts = monitor.active_alerts()
    assert len(alerts) == 1
    assert alerts[0].count > 1  # the burst is counted, not one alert per breaching sample


def test_late_earlier_sample_does_not_resurrect(
    run_fixture: Callable[..., Monitor],
) -> None:
    # Breach → clear → a late earlier breaching sample arrives out of order.
    monitor = run_fixture("out_of_order.jsonl")
    assert monitor.active_alerts() == []  # the cleared alert stays cleared
    # It fired once (before clearing), and did not re-fire on the stale sample.
    raised = LOG.with_code(ALERT_RAISED)
    assert len(raised) == 1
