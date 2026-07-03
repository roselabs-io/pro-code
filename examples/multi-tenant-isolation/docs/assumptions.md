# Multi-tenant Projects API — Assumptions Ledger

> The choices this build made that its inputs never specified — defaults reached for from habit or
> priors, not from the profile, spec, or ticket. Surfaced so a human can veto them.
> Dispositions: **promote** (belongs in the profile) · **decision** (this-build, recorded) ·
> **flag** (needs a human's second look) · **accept** (trivial, recorded so it's not invisible).

## Ledger

| # | Choice the build made | Where it came from | Declared? | Disposition |
|---|---|---|---|---|
| 1 | **PyJWT** as the JWT library | agent default | no (profile says "library is a build choice") | **decision** → `decisions/0002` |
| 2 | **HS256** (symmetric) signing algorithm | agent default | no (profile says "algorithm is a build choice") | **flag** — becomes RS256 if a *separate* service issues tokens; issuer is out of repo |
| 3 | Signing secret from `APP_TOKEN_SECRET`, with a **dev default** | agent default | no | **flag** — prod MUST override; the dev default must never ship |
| 4 | **In-memory** store, no database | agent default (brief said "backend slice") | no | **decision** → `decisions/0001` (scoped-guard shape is DB-agnostic) |
| 5 | Isolation enforced at the **app layer** (scoped store) vs DB RLS | forced by #4 | partly (isolation *is* declared; the mechanism isn't) | **decision** → `decisions/0001` |
| 6 | **Cursor pagination added to the list** (F3) | catalog hook `cursor-pagination` + "unbounded list" principle | no — the brief never asked for pagination | **flag** — is paging in scope for this slice, or scope creep? |
| 7 | List **ordered by project id** (uuid hex), cursor = last id | agent default | no | **accept** — stable + isolation-safe; a real product likely wants `created_at` ordering |
| 8 | Project **fields** = name, description (default `""`), created_by | agent default | no (brief said only "Projects") | **accept** — minimal reasonable shape |
| 9 | **Members** may create/read/update; only admins delete | inferred from brief ("admins can delete") | partly | **accept** — the only reading consistent with "admins *can* delete" |
| 10 | Isolation is checked **before** the role check (foreign id → 404 even for an admin) | agent default | no | **accept** — follows directly from "indistinguishable from not-found" (a 403 would leak existence) |
| 11 | Workspaces + actor-assignment are **out of repo** (owned by the token issuer) | agent default | no | **flag** — the slice can't onboard a tenant alone; confirm the issuer owns this |
| 12 | REST status codes: 201 create / 204 delete / 422 validation / 401 auth | agent default | no | **accept** — conventional REST |
| 13 | `PATCH` (partial) as the update verb; no `PUT` | agent default | no | **accept** |
| 14 | LOG sink = **JSON to stderr** + an in-process buffer for tests | agent default | partly (taxonomy declares "structured events") | **accept** — the format is the taxonomy's; the sink is a default |
| 15 | Ruff config lives **inline in `pyproject.toml`** (not a separate `ruff.toml`) | agent default | no | **accept** — one config file; matches the poetry-centric layout |

> The load-bearing **`no` rows are #2, #3, #6, #11** — the ones worth a human's veto. #2/#3 are the
> auth trust root (symmetric signing + a dev secret assume a shared-secret, same-deployment issuer).
> #6 is a scope question (pagination was never asked for). #11 is a boundary assumption (tenant
> onboarding lives somewhere this slice can't see). Everything else is either recorded as a decision
> or a conventional default. **Nobody's priors leaked in unseen — they're all on this page.**
