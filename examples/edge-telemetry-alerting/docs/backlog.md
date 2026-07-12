# edge-telemetry-alerting — Backlog

> **Forward-only** — shipped rows deleted as Implement lands them (git is the record).
> Pulled from `doc-patterns/living-docs/backlog.md`.

## Tickets

_All planned tickets (T1–T6) shipped this build and were pruned per the forward-only rule — see
`current-state.md` for what's built and git history for the planned rows. The queue below is the
work those tickets **surfaced**._

| ID | Title | Acceptance criterion (verifiable) | Design hooks | Depends on | Autonomy |
|---|---|---|---|---|---|
| N1 | Confirm the real signal catalog + thresholds | replace the assumed pump-house catalog with the plant's actual device spec; every fixture re-recorded from real telemetry; the same replay tests pass | `config-driven-thresholds` | — | 🔴 safety thresholds — domain-expert + human-owned |
| N2 | Periodic staleness reader | a background tick calls `state_at(now())` so a dropped sensor alerts without a viewer poll; asserted by a timed replay | `staleness-watchdog` | — | 🟡 agent-draft — bounded latency without a UI in the loop |
| N3 | Notification delivery | route a raised alert to a channel (pager/MQTT); out of scope for this slice | `novel — author fresh` | — | 🔴 out-of-repo dependency |

> N1 and N3 are the real deployment gaps logged in `open-questions.md`; they exist so the next agent
> inherits them tracked, not a green light. N1 is the promoted profile gap made concrete.

## Build order

- **Waves:** N1, N2, N3 are independent (Wave 0); N1 and N3 are gated on a domain/product decision.
- **Critical path:** n/a for the shipped slice — the T1→T2→T5→T6 chain is landed (git).
- **Start now:** N2 (graph-unblocked; a bounded engineering task).
- **Gated (not startable):** N1 → real device spec; N3 → channel choice.
