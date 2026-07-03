# Pump-station telemetry — Backlog

> One row per functionality, each well-formed: a fixture-replay acceptance criterion (fire +
> no-fire), a design hook, `depends-on`, an autonomy tier. Forward-only. **All shipped; retained
> here as the delivered slice's record.**

## Tickets

| ID | Title | Acceptance criterion (fixture-replay, verifiable) | Design hooks | Depends on | Autonomy |
|---|---|---|---|---|---|
| T1 | Station config loader | `station.toml` loads to typed rules; every safety-critical signal has a limit + TTL + CRITICAL severity | `config-driven-thresholds`, `named-severity-constant` | — | 🟢 proven, test-assertable |
| T2 | Severity constant | severities are `Severity.*`; no string literal in engine (special-lint clean) | `named-severity-constant` | — | 🟢 |
| T3 | Threshold + hysteresis rule | `overpressure.jsonl` → 1 CRITICAL at t=3; `nominal.jsonl` → 0; a value flapping in-band stays 1 alert | `threshold-with-hysteresis` | T1, T2 | 🟡 rule logic — agent-draft |
| T4 | Debounce | `pressure_spike.jsonl` (1-sample spike) → 0 alerts | `debounce-transient` | T3 | 🟢 |
| T5 | **Staleness watchdog** | `stale_sensor.jsonl` → CRITICAL; `dead_from_boot.jsonl` (never reported) → CRITICAL; nominal → none | `staleness-watchdog` | T1, T2 | 🔴 safety-critical path — human-owned |
| T6 | Alert dedup | `overpressure.jsonl` sustained → 1 active alert, count > 1 | `alert-dedup-storm-guard` | T3 | 🟢 |
| T7 | Out-of-order tolerance | `out_of_order.jsonl` (late earlier sample after clear) → alert stays cleared | `novel — author fresh` | T3 | 🟢 |
| T8 | /state read model | stale serializes `value:null, stale:true`; a critical breach serializes its status | `novel — author fresh` | T3, T5 | 🟢 |
| T9 | Live dashboard view | served view polls `/state`; a stale signal renders "— stale", a critical row renders red (browser grader) | `novel — author fresh` | T8 | 🟡 UI render — agent-draft |
| T10 | Alert observability | breach → `ALERT_RAISED{severity:critical}` in the trace; nominal → none | `named-severity-constant` | T3, T5 | 🟢 |
| T11 | **No-missed-critical certification** | every safety-critical fire fixture → CRITICAL (active + trace); nominal → silent | `staleness-watchdog`, `threshold-with-hysteresis` | T3, T5, T10 | 🔴 the core promise — human-certified, N-vote |

> **Autonomy:** 🟢 agent-ship · 🟡 agent-draft · 🔴 human-only (safety-critical path / out-of-repo dep).
> T5 + T11 are 🔴 by the profile rule — the safety-critical alert path is the core-promise boundary.
> They were human-certified (fixture-replay + a 3-vote refutation, below).

## Build order

- **Waves:**
  - Wave 0 (no deps): T1, T2
  - Wave 1: T3, T5
  - Wave 2: T4, T6, T7, T8, T10
  - Wave 3: T9, T11
- **Critical path:** T1 → T5 → T11 (the certification depends on the staleness watchdog).
- **Start now:** T1, T2.
- **Gated (not startable):** none — every rule is verifiable against a recorded fixture (no
  hardware in the loop), and the invented-thresholds open question does not block wiring the rules.
