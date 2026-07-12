# multi-tenant-isolation — Backlog

> One row per ticket, each well-formed. **Forward-only** — shipped rows are deleted as Implement
> lands them (git is the record). Pulled from `doc-patterns/living-docs/backlog.md`.

## Tickets

_All planned tickets (T1–T6) shipped this build and were pruned per the forward-only rule — see
`current-state.md` for what's built and git history for the planned rows. The queue below is the
work those tickets **surfaced**._

| ID | Title | Acceptance criterion (verifiable) | Design hooks | Depends on | Autonomy |
|---|---|---|---|---|---|
| N1 | Persist projects in a real store | isolation guard re-proven at the DB layer (RLS or scoped ORM); the same `test_isolation.py` passes against the persistent store | `tenant-scoped-query-guard` | — | 🔴 re-crosses the isolation boundary — human-owned |
| N2 | Token issuer + rotation | tokens minted + rotated by an issuer; expiry honored; `get_caller` rejects an expired/rotated key | `novel — author fresh` | — | 🔴 auth risk boundary + out-of-repo dependency |

> Both N1 and N2 are out-of-scope for this slice (logged in `open-questions.md`); they exist so the
> next agent inherits the real deployment gaps, not a green light.

## Build order

- **Waves:** N1 and N2 are independent (Wave 0), each gated by an open question (persistence choice; issuer choice).
- **Critical path:** n/a for the shipped slice — the T1→T3→T4→T5→T6 chain is landed (git).
- **Start now:** none — both remaining items are gated on a product/platform decision.
- **Gated (not startable):** N1 → persistence choice open; N2 → issuer choice open.
