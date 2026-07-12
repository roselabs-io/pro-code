# 0001 — A never-reported safety-critical signal is stale-critical from boot

> A durable decision + the load-bearing why. Pulled from `doc-patterns/living-docs/decision-record.md`.

- **Status:** accepted
- **Date:** 2026-07-11
- **Ticket:** T3 / T5

## Context

Staleness is easy to reason about once a signal has reported at least once (age = now − last_ts). But a signal that has **never** reported since boot has no `last_ts`. Treating that as "unknown / blank" would let a sensor that was dead from the start read as benign — the exact miss the no-missed-critical promise forbids.

## Decision

- A safety-critical signal with **no reading yet** is **stale** — and therefore CRITICAL — from boot, surfaced on the first `/state` read. `last_ts is None` → stale, regardless of `now`.

## Why (and what we rejected)

- The rejected reading ("no data yet = nominal / empty") is precisely how a dead-from-boot sensor slips through: the operator sees a blank cell, not an alarm. "Missing data is a fact, not a gap" (the domain principle) means absence must alert, and absence-from-boot is still absence.
- Asserted by `test_dead_from_boot_is_stale_critical` and the `dead_from_boot.jsonl` replay.

## Consequences

- The dashboard never shows a blank/zero for a configured-but-silent safety-critical signal — it shows "— stale" + CRITICAL.
- A signal legitimately expected to be quiet at boot would need a non-safety-critical classification or a grace window (not in this slice).
