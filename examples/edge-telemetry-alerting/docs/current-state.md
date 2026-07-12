# edge-telemetry-alerting — Current State

> Where things actually are **now**. The first doc a fresh agent reads to orient.
> Memory, not documentation. Pulled from `doc-patterns/living-docs/current-state.md`.

## What's built

- **Config + Severity + models (T1)** — `station.toml` → `Station` (config-driven thresholds); `Severity` is the one named-constant home for the level strings; a malformed ingest line is rejected by `parse_line`; a safety-critical signal with no alert condition fails the load loudly.
- **Level rule (T2)** — threshold with **hysteresis** (clear only past threshold∓h) + **debounce** (hold N samples before raising), high or low direction; severity-tiered (WARNING/CRITICAL).
- **Staleness watchdog (T3)** — evaluated **lazily on read** against the query clock; past-TTL → stale, value nulled, "— stale"; safety-critical stale → CRITICAL; a never-reported signal is stale-critical **from boot**.
- **Dedup + ordering (T4)** — a burst collapses to one active alert with an occurrence count; a late earlier-ts reading is ignored, so it can't resurrect a cleared alert.
- **No missed critical (T5)** — every fire fixture (bearing overheat, overpressure, dead-from-boot) raises `ALERT_RAISED{severity:critical}`; the nominal fixture is silent. Proven from the trace + the active-alert list.
- **Dashboard (T6)** — `GET /state` serializes each signal (stale → `value:null, "— stale"`); the served view renders stale as "— stale", critical as red, always with a text label; verified by the Playwright browser grader on the running app.

## What's in flight

- Nothing — all six tickets landed and green this session (31 fixture/API tests + 1 browser test).

## Known gaps / not-yet-built

- **The signal catalog + thresholds are a build assumption** (a pump-house station), not a profile input — a domain expert must confirm them before production (see `assumptions.md`, `open-questions.md`).
- **Notification delivery is out of scope** — alerts are raised + displayed, never routed to a channel.
- **Single station** — one `station.toml`; no multi-station switcher (declined in the UI sketch).

## How to run it

- Set up: `uv sync` (then `uv run playwright install chromium` for the browser test).
- Gate: `just gate` (fix · lint · typecheck · doctrine · security · test · coverage).
- Browser grader: `just browsertest`.
- Launch: `just demo` (or `uv run uvicorn dashboard.app:app --port 8000`) → dashboard on :8000.
