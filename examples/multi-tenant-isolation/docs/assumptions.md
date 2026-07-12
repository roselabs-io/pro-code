# multi-tenant-isolation — Assumptions Ledger

> The choices this build made that its inputs never specified — surfaced so a human can see and
> veto them. Pulled from `doc-patterns/living-docs/assumptions.md`. Graded by docs-currency + the
> drift grader's undeclared-choice lens.

## Ledger

| Choice the build made | Where it came from | Declared? | Disposition |
|---|---|---|---|
| FastAPI + uvicorn, Python ≥3.12 | profile Stack (`implement-profile.md`) | yes | — (declared choice-point) |
| poetry env, no task-runner | profile Stack | yes | — (declared) |
| In-memory store, not a DB | Plan seed + system-overview | yes | — (declared; see `decisions/0001`) |
| **HS256 (PyJWT) for the bearer token** | profile says "token library + algorithm are a build choice" | partial | **decision** — algorithm pinned in `decisions`-adjacent note; recorded here as the concrete pick. HS256 chosen (symmetric, one shared secret, matches the single-verifier slice). A multi-issuer deployment would prefer RS256/asymmetric. |
| **Signing secret from `PROJECTS_JWT_SECRET` env var** | agent default | no | **accept** — standard 12-factor config; the fail-closed-on-unset behaviour is tested. |
| **Cursor = the last item's id** (opaque) | agent default (impl of `cursor-pagination`) | no | **accept** — stable within the in-memory list; a DB build would encode a keyset cursor instead. |
| Delete is the only role-gated verb | Plan / open-questions | yes | — (declared; create/update member-allowed by product call, `open-questions.md`) |
| **libcst** as the codemod's parse/transform library | profile Implement ("one genuine libcst codemod per build") | yes | — (declared choice-point; the profile mandates a libcst codemod) |
| bandit · detect-secrets · pip-audit as the security/deps tools | profile `check-commands.md` | yes | — (declared; added to dev-deps so `poetry run` resolves them) |
| `owner_of` used for the audit trace only | agent default | no | **flag** — it reads across the tenant boundary *for logging only* (response is identical 404). Flagged for a human: confirm the trace-only use is acceptable; it must never feed a response. |

> The **`no` / `partial` rows** are the point. Two carry a real disposition: the JWT algorithm (a
> profile-declared build choice, pinned to HS256 here) and `owner_of`'s cross-boundary read (flagged —
> trace-only, never serialized). Nothing else was chosen outside the profile's declared choice-points.
