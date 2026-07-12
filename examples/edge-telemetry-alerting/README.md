# edge-telemetry-alerting

An industrial **edge telemetry monitor + alerting dashboard** built with the `edge-telemetry` profile.
The hard-done promise: **no missed critical alert** — every safety-critical breach (including a dropped
or dead-from-boot sensor) raises CRITICAL, and a stale signal renders **"— stale"**, never the last-good
number or "nominal".

Built through the pro-code pipeline: Frame → Plan → Implement, each handoff gated. See `docs/` for the
living spec (`functional-analysis`, `ui-sketches`, `system-overview`, `surfaces/dashboard`) and the build's
memory (`current-state`, `backlog`, `decisions/`, `assumptions`).

## The safety guarantees

- **Missing data alerts** — a signal past its TTL, or never reported since boot, is stale-critical (`decisions/0001`, `0002`).
- **No flapping** — level rules carry a hysteresis band; a value hovering at the line holds one alert, not N.
- **No transient spikes** — a debounce count holds N samples before firing.
- **No storm** — a burst dedups into one active alert with an occurrence count.
- **No resurrection** — a late earlier-ts reading can't reopen a cleared alert.
- **Proven from the trace** — every alert emits `ALERT_RAISED{signal,severity}` / `ALERT_CLEARED`; the logs grader asserts the critical fired.
- **Proven on screen** — a Playwright browser grader drives the running dashboard and asserts the stale row shows "— stale" and the critical row renders red + a text label (not colour-only).

## Run it

1. **Set up the environment**
   ```sh
   uv sync
   uv run playwright install chromium   # for the browser grader only
   ```
2. **Run the gate** (`just gate` runs them in short-circuit order)
   ```sh
   just gate          # fix · lint · typecheck · doctrine · security · test · coverage
   just browsertest   # the Playwright e2e (visual invariant on the running app)
   just deps          # supply-chain audit of the shipped tree
   ```
3. **Launch**
   ```sh
   just demo          # or: uv run uvicorn dashboard.app:app --port 8000
   ```
   The dashboard serves on :8000; `GET /state` returns the per-signal JSON.

## Layout

```
engine/     the rule engine — config · severity · models · monitor · replay · log
dashboard/  the served view — app (/state) · index.html · seed
config/     station.toml — the signal catalog + thresholds (config-driven)
fixtures/   recorded telemetry (JSONL) — fire + no-fire per rule
tests/      fixture-replay per rule + the /state + logs + Playwright browser graders
docs/       the living spec + build memory
```
