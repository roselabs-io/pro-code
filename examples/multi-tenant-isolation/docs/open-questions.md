# Multi-tenant Projects API — Open Questions

> Every assumption that could bite the build — state + owner + stakes. Also holds the
> **Design seeds → Plan** bucket. `[open]` / `[decided]`.

## Open / decided

- **[decided] Cross-tenant denied response = 404, not 403.** The brief requires a cross-tenant id
  be "indistinguishable from not-found"; 403 would confirm existence. Pinned before Plan (the
  profile's isolation hard gate). Owner: pipeline. Stakes: the core promise.
- **[decided] Isolation is enforced at the app layer** (a workspace-scoped store), not a DB.
  See `decisions/0001`. Stakes: how the invariant is verified.
- **[decided] Bearer tokens are signed JWTs (HS256).** See `decisions/0002`. Stakes: auth trust root.
- **[open] Token issuer is out of repo.** This slice assumes an upstream identity provider mints
  tokens with `{ws, sub, role}` claims and shares the signing secret. Owner: platform. Stakes: if
  the issuer is a separate service, HS256 (symmetric) should become RS256 (asymmetric) — flagged in
  `assumptions.md`.
- **[open] No workspace lifecycle here.** Create/rename/delete of a workspace, and how an actor is
  assigned to one, live upstream. Owner: platform. Stakes: this slice can't onboard a tenant alone.
- **[open] Persistence is in-memory.** State resets on restart; no durability. Owner: pipeline.
  Stakes: fine for the isolation slice; a real deployment needs a datastore (the scoped-query guard
  shape carries over — see `decisions/0001`).

## Design seeds → Plan

- **Scope every query by workspace, deny-by-default** → confirmed as `tenant-scoped-query-guard`.
- **Enforce role at the request boundary** → confirmed as `rbac-check-at-boundary`.
- **Type the error envelope, choose 404-over-403 deliberately** → confirmed `structured-error-envelope`.
- **Emit a structured event as each write/denial lands** → confirmed `write-through-audit-log`.
- **Page the list with an opaque cursor** → confirmed `cursor-pagination` (see the F3 scope note in
  `assumptions.md` — pagination was added, not in the brief).
