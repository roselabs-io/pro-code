"""Demo seed — a deterministic monitor state for the dashboard + browser grader.

One nominal signal, one CRITICAL (overpressure), one stale (dropped) — so the rendered
view exercises both the red-critical path and the '— stale' invariant.
"""

from __future__ import annotations

from engine.models import Reading
from engine.monitor import Monitor

# The fixed clock the served demo evaluates staleness against.
DEMO_NOW = 1012.0


def seeded_monitor() -> Monitor:
    """Build a monitor: bearing nominal, pressure critical, flow stale."""
    monitor = Monitor()
    monitor.process(Reading(signal="bearing_temp", value=73.0, ts=1010.0))
    monitor.process(Reading(signal="discharge_pressure", value=11.4, ts=1010.0))
    monitor.process(Reading(signal="flow_rate", value=25.0, ts=900.0))
    return monitor
