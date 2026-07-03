# {{project_name}} — Assumptions Ledger

> The choices this build made that its inputs never specified — defaults the agent reached
> for from habit or priors, not from the profile, spec, or ticket. Surfaced so a human can
> see and veto them, not left silent. Pulled from `doc-patterns/living-docs/assumptions.md`.
> Graded by the docs-currency grader + the drift grader's undeclared-choice lens.

Every non-trivial choice either traces to a **declared source** (profile choice-points / spec / ticket / decision-record) or it lands here with a **disposition**:

- **promote** — a reusable default; belongs in the profile's choice-points. Promote it, then drop the row.
- **decision** — this-build-only and non-obvious; write a `decisions/NNNN` record and link it.
- **flag** — a bias worth a human's second look; route to the driver / `open-questions`.
- **accept** — trivial and fine as-is; recorded so it's not invisible.

## Ledger

| Choice the build made | Where it came from | Declared? | Disposition |
|---|---|---|---|
| {TODO: e.g., FastAPI as the web framework} | agent default | no | promote → profile Stack |
| {TODO: e.g., in-memory store, not a DB} | spec / Plan seed | yes | — (declared) |
| {TODO: e.g., HS256 for the JWT} | agent default | no | flag — driver confirms the algorithm |

> The point is the **`no`** rows: a choice with no declared source is a silent bias until it's
> here. An empty ledger means *either* everything was declared *or* nobody looked — say which.
