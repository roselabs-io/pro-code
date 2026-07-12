"""Dashboard API — GET /state serializes the monitor's per-signal view; / serves the view.

Staleness is computed against a query clock (`?now=`), defaulting to the demo clock so the
served page is stable; the stale value serializes as null with the '— stale' label.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse

from dashboard.seed import DEMO_NOW, seeded_monitor

app = FastAPI(title="edge-telemetry-dashboard")
_monitor = seeded_monitor()
_INDEX = Path(__file__).resolve().parent / "index.html"


@app.get("/state")
def state(now: float = Query(default=DEMO_NOW)) -> dict:
    """The current per-signal state at `now` — stale signals nulled to '— stale'."""
    statuses = _monitor.state_at(now)
    return {
        "station": _monitor.station.name,
        "now": now,
        "signals": [
            {
                "name": s.name,
                "unit": s.unit,
                "value": s.value,
                "stale": s.stale,
                "severity": s.severity.value,
                "label": s.label,
            }
            for s in statuses
        ],
        "active_alerts": len(_monitor.active_alerts()),
    }


@app.get("/")
def index() -> FileResponse:
    """Serve the static monitoring view."""
    return FileResponse(_INDEX)
