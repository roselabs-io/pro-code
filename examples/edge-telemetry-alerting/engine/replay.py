"""Replay — feed a recorded fixture (JSONL) through the monitor, deterministically.

The verify harness: no live device, just a recorded stream. `parse_line` validates each
line at ingest; a malformed line is rejected, not fed to the rules.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from engine.config import Station
from engine.models import Reading
from engine.monitor import Monitor


def parse_line(line: str) -> Reading:
    """Validate one telemetry line into a Reading; raise ValueError if malformed."""
    try:
        return Reading.model_validate(json.loads(line))
    except (json.JSONDecodeError, ValidationError) as exc:
        raise ValueError(f"malformed telemetry line: {line!r}") from exc


def replay(path: Path, station: Station | None = None) -> Monitor:
    """Replay a fixture through a fresh monitor; a malformed line is skipped, not fed."""
    monitor = Monitor(station)
    for raw in path.read_text().splitlines():
        if not raw.strip():
            continue
        try:
            reading = parse_line(raw)
        except ValueError:
            continue
        monitor.process(reading)
    return monitor
