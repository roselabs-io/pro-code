# Pump-station telemetry — Current State

> Where things actually are now. The first doc a fresh agent reads. Kept current every ticket.

## What's built

- **Rule engine** (`engine/monitor.py`) — per signal: threshold-with-hysteresis, debounce,
  staleness watchdog (incl. **dead-from-boot**), alert dedup, out-of-order tolerance.
- **Station config** (`config/station.toml`) — 3 signals: discharge_pressure (CRITICAL),
  bearing_temperature (CRITICAL), flow_rate (WARNING). Thresholds/hysteresis/debounce/TTLs in TOML.
- **Severity** is an enum constant everywhere (`severity-constant` lint clean).
- **Dashboard** (`dashboard/app.py` + `index.html`) — `/state` JSON + a served view that polls and
  renders (stale → "— stale", critical → red). `POST /ingest` accepts live readings.
- **Fixtures** (`fixtures/*.jsonl`) — fire + no-fire per rule, incl. `dead_from_boot`, `flap`,
  `out_of_order`, `pressure_spike`.
- **Observability** — `ALERT_RAISED{signal,severity}` / `ALERT_CLEARED`.

## What's in flight

- Nothing — the slice is complete; `just gate` is green (28 fixture-replay tests + 2 browser).

## Known gaps / not-yet-built

- **Invented thresholds** — the signal catalog + all numeric limits/TTLs are placeholders pending a
  real device spec sheet + runbook (see `assumptions.md`).
- **No notification delivery** — the slice raises alerts, it does not send them (out of scope).
- **No persistence** — monitor state is in-memory; a restart re-arms dead-from-boot from the new boot.
- **Direct/`POST /ingest` transport** — no MQTT/HTTP front, no backpressure.

## How to run it

```bash
uv sync
uv run playwright install chromium   # one-time, for the browser grader
just gate                            # fix · lint · doctrine · fixture-replay · browser
just demo                            # serve the seeded dashboard (stale + critical) on :8000
```
