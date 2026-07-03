# 0002 — Staleness evaluated lazily on read, not by a background ticker

- **Status:** accepted
- **Date:** 2026-07-03
- **Ticket:** T5 (staleness watchdog), T8 (/state)

## Context

The staleness watchdog needs a notion of "now" to decide a signal has gone silent. That "now" can
come from a background loop that ticks on a timer, or be supplied at read time.

## Decision

`check_staleness(now)` is called explicitly — on each `GET /state` (`snapshot` runs it) and from
fixtures via a `{tick: <ts>}` line. There is no background thread.

## Why (and what we rejected)

- **Rejected — a background ticker thread:** raises alerts on a wall-clock timer, which is
  non-deterministic to test and adds concurrency to an otherwise pure engine. The fixture-replay
  posture (fire + no-fire, exact timing) needs a clock the test controls.
- Lazy-on-read keeps the engine pure and deterministic: the same fixture always yields the same
  alerts. The live dashboard gets fresh staleness because it reads `/state` every 2s anyway.

## Consequences

- `GET /state` has a side effect (it may raise a staleness alert). Acceptable and idempotent — a
  second read while already stale does not re-raise or re-log.
- A signal only goes stale when something reads `/state` or ticks; with a 2s dashboard poll that is
  effectively continuous. A headless deployment with no reader would need a periodic tick.
