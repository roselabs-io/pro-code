# 0001 — Dead-from-boot staleness measured from station_start

- **Status:** accepted
- **Date:** 2026-07-03
- **Ticket:** T5 (staleness watchdog), T11 (no-missed-critical)

## Context

The core promise is "no missed critical alert." The obvious staleness rule — "a signal is stale if
`now − last_seen > ttl`" — has a hole: a sensor that has **never** reported has no `last_seen`, so
a naive watchdog never evaluates it. A safety sensor that is dead from boot would stay silent — the
exact failure the profile calls out (and the analogue of the bug the reference build's N-vote caught).

## Decision

Every signal is watched from the station's boot. When a signal has never reported, staleness is
measured from `station_start` instead of `last_seen`: it is stale once `now − station_start > ttl`,
and (being safety-critical) raises CRITICAL — a dead-from-boot alert.

## Why (and what we rejected)

- **Rejected — watch only signals that have reported at least once:** simpler, but it is precisely
  the missed-critical hole. A configured safety signal that never boots would never alert.
- Measuring from `station_start` closes it with no special-casing at call sites: the watchdog loops
  over the *config's* signals (not the *seen* signals), so an absent signal is a first-class case.

## Consequences

- `dead_from_boot.jsonl` is a first-class fire fixture in the no-missed-critical certification.
- On restart, `station_start` resets, so dead-from-boot re-arms from the new boot (acceptable for an
  in-memory slice; a persistent deployment would carry `station_start` forward).
