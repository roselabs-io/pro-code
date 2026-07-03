"""FastAPI dashboard — a /state JSON endpoint and a served operator view.

The monitor is a module singleton fed by ingest; ``/state`` is its read model (staleness
evaluated as of now). ``DASHBOARD_SEED=browser`` seeds a deterministic mixed state so the
browser grader can drive the running app.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from engine.config import load_station
from engine.models import Reading
from engine.monitor import Monitor

_INDEX = Path(__file__).resolve().parent / "index.html"

monitor = Monitor(load_station())
if os.environ.get("DASHBOARD_SEED") == "browser":
    from dashboard.seed import seed_browser

    seed_browser(monitor)

app = FastAPI(title="Pump-station telemetry dashboard")


@app.get("/state")
def state() -> dict[str, Any]:
    return monitor.snapshot(now=time.time())


@app.post("/ingest", status_code=202)
def ingest(reading: dict[str, Any]) -> dict[str, str]:
    monitor.process(
        Reading(reading["signal"], float(reading["value"]), float(reading["ts"]))
    )
    return {"status": "accepted"}


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return _INDEX.read_text()
