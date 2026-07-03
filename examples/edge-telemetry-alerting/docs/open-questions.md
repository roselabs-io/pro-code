# Pump-station telemetry — Open Questions

> Every assumption that could bite the build + the **Design seeds → Plan** bucket. `[open]`/`[decided]`.

## Open / decided

- **[decided] Two safety-critical signals** (discharge_pressure, bearing_temperature) each carry a
  threshold **and** a staleness rule at CRITICAL; flow_rate is operational WARNING. Pinned before
  Plan (the alert-coverage hard gate). Owner: pipeline. Stakes: the core promise.
- **[decided] Dead-from-boot is measured from `station_start`.** A signal that never reported is
  stale once `now − station_start > ttl`. See `decisions/0001`. Stakes: this is the exact miss the
  profile warns about.
- **[decided] Staleness is evaluated lazily on read** (`snapshot`/`check_staleness`), not by a
  background ticker. See `decisions/0002`. Stakes: when the watchdog fires.
- **[open] The signal catalog + all thresholds are invented.** The specific signals, limits
  (10.0 bar, 85 °C, 20 m³/h), hysteresis bands, debounce (3), and TTLs (5/10/15 s) are placeholder
  values — a real build gets them from a device spec sheet + ops runbook. Owner: SRE. Stakes: wrong
  numbers = wrong alerts. **Flagged in `assumptions.md`.**
- **[open] Is low flow safety-critical?** Modelled here as operational WARNING; a station where a
  dry-run damages the pump would make it CRITICAL. Owner: SRE. Stakes: severity of a real hazard.
- **[open] Device transport is a direct call / `POST /ingest`.** A real deployment fronts ingest
  with MQTT/HTTP + backpressure. Owner: platform. Stakes: out of this slice.
- **[open] Monitor state is in-memory.** No persistence across restart. Owner: pipeline. Stakes:
  fine for the slice; a restart loses alert history (dead-from-boot re-arms from the new boot).
- **[decided] A delayed-but-in-order frame momentarily clears a staleness alert.** `process` ends
  a STALENESS alert on any accepted reading (`ts ≥ last_ts`); a badly-backlogged frame with an old
  `ts` clears it in the raw `active_alerts()` list for one evaluation. It **self-heals**: the frame
  sets `last_ts` to its own old value, so the next `check_staleness(now)` re-fires CRITICAL, and
  `snapshot` always runs `check_staleness` before rendering — so the operator read model never
  exposes the gap. Surfaced by the adversarial no-missed-critical refuter (author ≠ grader); not a
  durable miss (ties to `decisions/0002`). Owner: pipeline. Stakes: none today; revisit if a
  headless deployment reads `active_alerts()` directly without a `snapshot`/tick.

## Design seeds → Plan

- **Fire past a limit, clear past limit ∓ h** → confirmed `threshold-with-hysteresis`.
- **Hold N samples before firing** → confirmed `debounce-transient`.
- **Absence is an alert, incl. never-reported** → confirmed `staleness-watchdog`.
- **A burst is one alert + a count** → confirmed `alert-dedup-storm-guard`.
- **Severity is an enum constant** → confirmed `named-severity-constant`.
- **Thresholds live in config** → confirmed `config-driven-thresholds`.
