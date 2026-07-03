# {{NNNN}} — {{short decision title}}

> A durable decision + the load-bearing **why** — so the next agent doesn't re-litigate it.
> One file per decision (`docs/decisions/NNNN-*.md`). For *non-obvious calls and deviations* only —
> skip the obvious, skip "we used hook X" (that's the ticket's hook). Written **as you decide**, not retrofitted.
> Pulled from `doc-patterns/living-docs/decision-record.md`.

- **Status:** {proposed | accepted | superseded by NNNN}
- **Date:** {TODO: YYYY-MM-DD}
- **Ticket:** {TODO: which ticket surfaced this}

## Context

The forces in play — what made this a real fork, not a default.

- {TODO: what problem / constraint forced a choice}

## Decision

The call, in one or two sentences.

- {TODO: "We scope isolation at the app layer (query guard), not Postgres RLS."}

## Why (and what we rejected)

The load-bearing reasoning + the alternative you turned down and its cost.

- {TODO: "RLS is stronger but couples us to Postgres and complicates local tests; the guard is verifiable by integration test today. Revisit if we add a second data store."}

## Consequences

What this makes easier, harder, or forbidden downstream.

- {TODO}
