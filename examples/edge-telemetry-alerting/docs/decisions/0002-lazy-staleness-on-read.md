# 0002 — Staleness is evaluated lazily on read, against an explicit clock

> A durable decision + the load-bearing why. Pulled from `doc-patterns/living-docs/decision-record.md`.

- **Status:** accepted
- **Date:** 2026-07-11
- **Ticket:** T3

## Context

Staleness is time-relative: a signal is stale once its age exceeds its TTL. That can be driven by a **background timer** (a scheduler ticks and marks signals stale) or **lazily on read** (age is computed when `/state` is queried). The choice affects testability and how the promise is proven.

## Decision

- Compute staleness **lazily on read**: `Monitor.state_at(now)` and `/state?now=` take an explicit `now` and derive each signal's staleness from `now − last_ts`. No background thread. The staleness alert is raised/cleared as a side effect of that read.

## Why (and what we rejected)

- A background timer introduces wall-clock nondeterminism — the exact thing that makes a rule un-replayable. With an explicit clock, a fixture replay is fully deterministic: feed readings, then query `state_at(t)` and assert. That's what lets the fixture-replay grader certify the promise.
- The cost: staleness only surfaces when something reads `/state`. In this slice the dashboard polls, so a dropped sensor surfaces on the next poll — acceptable. A push/paging deployment would add a periodic reader (a tick that calls `state_at(now())`), reusing the same lazy logic.
- Asserted by every `test_staleness` case + the `/state` endpoint tests.

## Consequences

- The engine is pure and clock-injected — trivially testable, no time mocking.
- Alerting latency is bounded by the poll interval, not by a timer; a real deployment must add a periodic read to bound it independently of a viewer.
