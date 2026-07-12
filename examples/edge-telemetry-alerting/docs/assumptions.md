# edge-telemetry-alerting — Assumptions Ledger

> The choices this build made that its inputs never specified — surfaced so a human can see and
> veto them. Pulled from `doc-patterns/living-docs/assumptions.md`. Graded by docs-currency + the
> drift grader's undeclared-choice lens.

## Ledger

| Choice the build made | Where it came from | Declared? | Disposition |
|---|---|---|---|
| Python engine + FastAPI dashboard, uv + justfile | profile Stack (`implement-profile.md`) | yes | — (declared choice-point) |
| **The concrete signal catalog + thresholds** (pump-house: bearing_temp warn 80/crit 95, discharge_pressure warn 8.5/crit 10, flow_rate low 20; hysteresis + debounce + TTL per signal) | agent default — the profile supplies rule *shapes*, not a station catalog | **no** | **flag → promote** — this is a real **profile gap**: `edge-telemetry` gives no example signal catalog. Chosen defaults are plausible but unverified; a domain expert confirms before production. A worked example catalog belongs in the profile. |
| Staleness severity = CRITICAL for safety-critical, WARNING otherwise | agent default (the profile says safety-critical stale is critical; the non-critical severity was unspecified) | partial | **decision** — recorded; a per-signal staleness severity in config would generalize it. |
| Lazy staleness on read (explicit `now`) | Plan seed + system-overview | yes | — (declared; see `decisions/0002`) |
| Dead-from-boot = stale-critical | Frame open-question + Plan | yes | — (declared; see `decisions/0001`) |
| **Debounce applies to raising only; clearing is hysteresis-governed** | agent default (impl of the two hooks) | no | **flag** — a reasonable reading of "debounce + hysteresis," but the profile doesn't pin whether clearing is also debounced. Flagged for review. |
| Occurrence count increments per breaching reading while active | agent default (impl of `alert-dedup-storm-guard`) | no | **accept** — a defensible storm metric; a time-window count is an alternative a real deploy might prefer. |
| Dashboard colour hexes + poll interval (2s) | agent default | no | **accept** — cosmetic; the load-bearing invariant (text label + "— stale") is tested, the exact palette is not. |
| JSONL as the telemetry line format; pydantic as the ingest validator | agent default (pydantic ships with the declared FastAPI stack) | no | **accept** — a defensible transport/validation pair; the shape `{signal,value,ts}` is what the fixtures + `parse_line` agree on. |
| Debounce guards the initial raise only; escalation once alerting is immediate | agent default (impl of `debounce-transient`; hardened after the N-vote caught an oscillation miss) | no | **decision** — a sustained oscillating breach must still fire, and a missed critical is worse than a false one, so escalation isn't debounced. See the loop findings in the build report. |

> The headline `no` row is the **profile gap**: `edge-telemetry` supplies the alerting *shapes* but no
> concrete signal catalog, so any runnable build must invent one. That belongs in the report as a profile
> bug to promote — a worked example station catalog would remove the guesswork.
