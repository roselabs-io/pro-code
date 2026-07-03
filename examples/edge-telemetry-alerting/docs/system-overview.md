# Pump-station telemetry — System Overview

> The 30,000-foot picture. Plan's output, from the functional analysis.

## Components

| Component | What it does |
|---|---|
| Station config (`config/station.toml` + `engine/config.py`) | signals, thresholds, hysteresis, debounce, TTLs, severity — the `config-driven-thresholds` source of truth |
| `Severity` enum (`engine/severity.py`) | the one home for severity strings; everything else uses the constant |
| Monitor (`engine/monitor.py`) | the rule engine — per-signal threshold+hysteresis+debounce, staleness watchdog, dedup, out-of-order tolerance |
| Replay (`engine/replay.py`) | drives a fixture stream (readings + clock ticks) through a monitor — the verify path |
| Event log (`engine/log.py`) | emits `ALERT_RAISED{signal,severity}` / `ALERT_CLEARED` for the logs grader |
| Dashboard (`dashboard/app.py` + `index.html`) | `/state` JSON read model + a served view that polls and renders |

## Key dataflows

- **Ingest → evaluate:** a reading `{signal, value, ts}` → `Monitor.process` updates per-signal
  state → threshold rule (with hysteresis + debounce) may raise/clear a deduped alert → an
  `ALERT_*` event fires.
- **Staleness:** `check_staleness(now)` (called on each `/state` read) → for every signal, if
  `now − last_seen > ttl` (or `now − station_start > ttl` when never seen) → raise a staleness
  alert at the signal's severity.
- **Render:** `GET /state` → `Monitor.snapshot(now)` → per-signal `{value, stale, status}` +
  active alerts → the browser polls every 2s and renders (stale → "— stale"; critical → red).

## Integration boundaries

- **Device transport (inbound).** Protocol: a reading `{signal, value, ts}` via a direct call or
  `POST /ingest` in this slice (MQTT/HTTP in a real deployment). Trigger: each sample. A malformed
  reading is rejected at ingest. See the open question on transport.
- **Notification delivery (outbound) — out of scope.** The slice raises alerts; it does not send
  them. No integration built.

## Tech-stack call-outs

- **Config in TOML via stdlib `tomllib`** — no extra dependency; re-tuning is a config edit.
- **Staleness evaluated lazily on read**, not by a background loop — deterministic and testable.
  See `decisions/0002`.
