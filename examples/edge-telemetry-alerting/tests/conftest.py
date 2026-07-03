from __future__ import annotations

from collections.abc import Callable

import pytest

from engine.log import LOG
from engine.monitor import Monitor
from engine.replay import new_monitor, replay


@pytest.fixture(autouse=True)
def _reset_log() -> None:
    LOG.clear()


@pytest.fixture
def run_fixture() -> Callable[..., Monitor]:
    def _run(fixture: str, station_start: float = 0.0) -> Monitor:
        return replay(new_monitor(station_start=station_start), fixture)

    return _run


def critical_alerts(monitor: Monitor) -> list:
    return [a for a in monitor.active_alerts() if a.severity.name == "CRITICAL"]
