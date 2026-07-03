# edge-telemetry-alerting

An industrial **pump-station telemetry monitor + alerting engine** with a served live dashboard,
built through the pro-code pipeline on the **`edge-telemetry`** profile. Edge devices stream sensor
readings; a rule engine raises alerts. **Hard-done: no missed critical alert** — every real
safety-critical breach (a bad value held, or a stale / dead-from-boot safety sensor) raises a
CRITICAL alert; a nominal stream stays silent. Certified by fixture-replay + a Playwright browser
grader.

- **Stack:** Python 3.12 · pure-Python rule engine · FastAPI dashboard (`/state` + served HTML/JS).
  Env: **uv** + a **justfile** (`just gate`).
- **Rules:** threshold-with-hysteresis · debounce · staleness-watchdog (incl. dead-from-boot) ·
  alert dedup · out-of-order tolerance. Thresholds live in `config/station.toml`, never in code.

## Layout

```
engine/       the rule engine — severity · config · models · monitor · replay · log
dashboard/    the served view — FastAPI /state + index.html + the browser seed
fixtures/     recorded telemetry (fire + no-fire per rule, incl. dead_from_boot)
config/        station.toml — signals, thresholds, hysteresis, debounce, TTLs
tests/        fixture-replay per rule + logs grader + the Playwright browser grader
docs/         the pipeline's output — spec, ui-sketch, plan, living docs, assumptions ledger
```

## Run it

```bash
uv sync
uv run playwright install chromium   # one-time, for the browser grader
```

Gate (one command — recipes call `uv run`):

```bash
just gate     # fix (codemod-lite) · lint · doctrine + severity-constant · fixture-replay · browser
```

Or the steps individually:

```bash
just fix            # ruff --fix + format (auto-fix arm)
just lint           # ruff check
just doctrine-lint  # comment doctrine + test posture + severity-constant forbid
just test           # pytest -m "not browser"  (fixture-replay: fire + no-fire per rule)
just browser        # pytest -m browser         (Playwright, real Chromium)
just typecheck      # mypy engine (advisory author-aid, not a gate step)
```

Launch:

```bash
just demo    # serve the seeded dashboard (a CRITICAL breach + a dead-from-boot stale row) on :8000
just up      # serve the live monitor;  just down  to stop
```

The gate is green: **28 fixture-replay tests + 2 browser tests**, ruff / doctrine / severity-constant
all clean.
