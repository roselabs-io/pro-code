"""Deterministic dashboard seed for the browser grader.

Drives the monitor into a known mixed state: one signal in a CRITICAL breach (red), one
safety-critical signal dead-from-boot (renders "— stale"), one nominal. The browser grader
seeds this, then asserts the *rendered* view honours it.
"""

from __future__ import annotations

import time

from engine.models import Reading
from engine.monitor import Monitor


def seed_browser(monitor: Monitor) -> None:
    now = time.time()
    # Boot the station in the past so an absent safety sensor is already stale.
    monitor.station_start = now - 3600
    # discharge_pressure: a held overpressure breach → active CRITICAL, value shown red.
    for i, value in enumerate([10.5, 11.0, 11.5, 11.6]):
        monitor.process(Reading("discharge_pressure", value, now - 1 + i * 0.1))
    # flow_rate: nominal.
    monitor.process(Reading("flow_rate", 42.0, now))
    # bearing_temperature: never reported → dead-from-boot staleness (CRITICAL).
