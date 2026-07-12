# edge-telemetry-alerting — Open Questions

> Every assumption that could bite the build — state + owner + stakes. Also holds the
> **Design seeds → Plan** bucket. Resolved items flip to `[decided]`.

## Open / decided

- **[decided]** **Every safety-critical signal carries an alert condition + severity.** bearing_temp and discharge_pressure each have a level rule (warn/critical) AND a staleness watchdog (→ CRITICAL). *(Frame hard gate — alert-coverage of safety-critical signals.)*
- **[decided]** **Staleness is evaluated lazily on read**, against the query clock — not by a background timer. A signal's age is computed when `/state` is queried, so a dropped sensor surfaces on the next poll. *(See `decisions/0002`.)*
- **[decided]** **A never-reported signal is stale from boot** ("dead from boot") — for a safety-critical signal that's CRITICAL, not an empty/unknown cell. *(See `decisions/0001`.)*
- **[decided]** **A stale signal renders "— stale", never the last-good number or "nominal".** The visual invariant the browser grader asserts.
- **[decided]** **An out-of-order (older-ts) reading does not change alert state** — it can't resurrect a cleared alert. The monitor tracks the max ts seen per signal.
- **[open]** **The concrete signal catalog + thresholds are a build assumption, not a profile input.** The profile supplies the rule *shapes*, not the station's actual signals/limits. Chosen defaults (a pump-house station: bearing_temp, discharge_pressure, flow_rate) are in `docs/assumptions.md`, flagged for a domain expert to confirm. Owner: plant SRE. Stakes: the thresholds must match the real device spec before production. **This is a profile gap to promote.**
- **[open]** **Notification delivery is out of scope.** Alerts are raised + displayed, not routed. Owner: platform. Stakes: a real deployment needs a channel; absent here (profile-declared).

## Design seeds → Plan (hypotheses, not decisions)

- Seed: *thresholds/TTLs/hysteresis live in `station.toml`, not code literals* → `config-driven-thresholds`. Plan confirms.
- Seed: *severities are a named enum, never string literals* → `named-severity-constant`. Plan confirms.
- Seed: *level rules carry a hysteresis band + a debounce count* → `threshold-with-hysteresis` + `debounce-transient`. Plan confirms.
- Seed: *absence within a TTL is itself an alert* → `staleness-watchdog`. Plan confirms.
- Seed: *a burst dedups into one active alert + a count* → `alert-dedup-storm-guard`. Plan confirms.
