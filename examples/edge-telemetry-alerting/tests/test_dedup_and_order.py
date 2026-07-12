"""Dedup + ordering — a burst is one alert; a late earlier sample can't resurrect."""

from __future__ import annotations

from engine import log
from engine.config import load_station
from engine.models import Reading
from engine.monitor import Monitor


def test_burst_collapses_to_one_alert_with_a_count() -> None:
    m = Monitor(load_station())
    for i in range(4):
        m.process(Reading(signal="discharge_pressure", value=11.0, ts=1000.0 + i))
    alerts = m.active_alerts()
    assert len(alerts) == 1, "a storm of one condition is ONE active alert, not N"
    assert alerts[0].count == 4, "the occurrences are counted, not dropped"


def test_out_of_order_earlier_sample_does_not_resurrect_a_cleared_alert() -> None:
    m = Monitor(load_station())
    m.process(
        Reading(signal="discharge_pressure", value=11.0, ts=1000.0)
    )  # raise critical
    m.process(Reading(signal="discharge_pressure", value=7.0, ts=1001.0))  # clear
    assert m.active_alerts() == []
    log.reset()
    m.process(
        Reading(signal="discharge_pressure", value=12.0, ts=1000.5)
    )  # LATE earlier sample
    assert (
        m.active_alerts() == []
    ), "a late earlier reading must not reopen a cleared alert"
    assert [e for e in log.events() if e["code"] == log.ALERT_RAISED] == []
