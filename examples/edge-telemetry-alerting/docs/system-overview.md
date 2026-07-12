# edge-telemetry-alerting — System Overview

> The 30,000-foot picture. Pulled from `doc-patterns/specs/system-overview.md`; filled from the functional analysis.

## Components

| Component | What it does |
|---|---|
| Station config (`engine/config.py` + `config/station.toml`) | loads the signal catalog + rules (thresholds, hysteresis, debounce, staleness TTL, severity) — all config-driven, no literals in rule code |
| Severity enum (`engine/severity.py`) | the one source of truth for severity constants (`Severity.CRITICAL/WARNING/INFO`); the only place the strings live (`doctrine: allow`) |
| Monitor (`engine/monitor.py`) | the rule engine — ingests readings, maintains per-signal state, applies level+hysteresis+debounce, staleness, dedup, out-of-order tolerance; opens/clears alerts |
| Replay (`engine/replay.py`) | feeds a recorded fixture (JSONL) through the monitor and returns the resulting state/alerts — the deterministic verify harness |
| Structured log (`engine/log.py`) | emits `ALERT_RAISED{signal,severity}` / `ALERT_CLEARED` the logs grader reads |
| Dashboard API (`dashboard/app.py`) | FastAPI `/state` — the monitor's current per-signal state as JSON (staleness computed against the query clock) |
| Dashboard view (`dashboard/index.html`) | the served static view — polls `/state`, renders value/status, stale as "— stale", critical as red, with a text label (not colour-only) |

## Key dataflows

- **Ingest→evaluate→display:** a reading `{signal,value,ts}` enters the monitor → the monitor updates that signal's state (level with hysteresis + debounce, or ignores an out-of-order older sample) → a transition opens/clears an alert and emits the event → `/state` (queried at time `now`) computes staleness lazily and returns each signal's value + status → the view renders it.
- **Staleness on read:** `/state` at `now` compares each signal's last-reading age to its TTL; over-TTL (or never-reported) → stale; safety-critical stale → CRITICAL. The value is nulled and rendered "— stale".

## Integration boundaries

- **Device transport (ingest)** — inbound stream of JSON lines `{signal, value, ts}` (unix seconds). We parse + validate each line (`parse_line`); a malformed line is rejected at ingest, not fed to the rules. A recorded fixture (`fixtures/*.jsonl`) is the same shape replayed deterministically — that's how rules are graded without a live device.
- **Notification delivery** — out of scope; the slice raises + displays alerts, it does not route them.

## Tech-stack call-outs

- **Time is explicit, not wall-clock.** The monitor and `/state` take a `now` timestamp (from the readings / the request), so staleness and ordering are deterministic and fixture-replayable. *(See `decisions/0002`.)*
- **Config-driven thresholds** — every limit/TTL/hysteresis band lives in `station.toml`, so re-tuning is a config edit, not a code change (`config-driven-thresholds`).
