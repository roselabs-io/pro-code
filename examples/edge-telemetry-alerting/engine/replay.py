"""Replay a recorded telemetry fixture through a monitor — the deterministic verify path.

A fixture is JSON lines: a reading ``{signal, value, ts}``, or a clock advance
``{tick: <ts>}`` that runs the staleness watchdog at that time. No hardware in the loop —
a recorded stream proves a rule both fires and stays quiet.
"""

from __future__ import annotations

import json
from pathlib import Path

from engine.config import load_station
from engine.models import Reading
from engine.monitor import Monitor

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def new_monitor(station_start: float = 0.0) -> Monitor:
    return Monitor(load_station(), station_start=station_start)


def replay(monitor: Monitor, fixture: str) -> Monitor:
    path = FIXTURES / fixture if not fixture.endswith("/") else Path(fixture)
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        record = json.loads(line)
        if "tick" in record:
            monitor.check_staleness(float(record["tick"]))
        else:
            monitor.process(
                Reading(record["signal"], float(record["value"]), float(record["ts"]))
            )
    return monitor
