# Profile — `saas-web` · Plan

Domain: a **full-stack web SaaS** — FastAPI (async) + React/TS/MUI + async Postgres, deployed via Docker
Compose. Pairs with `frame-profile.md`.

## Surface = a feature slice (a view + its endpoint group)

A "surface" here spans **a view (or view group) and the endpoints behind it** — e.g. the *posts* surface is the public post list/detail views, the author's editor, and the `/posts` endpoints they call. Per-surface spec = one `docs/surfaces/<name>.md`. (`generic-saas` scopes a surface to an endpoint group; `edge-telemetry` to a dashboard view; this profile spans both halves of the same slice — that's the swap.)

## Design catalog (the source of hooks)

The shapes Plan routes tickets against — a full-stack set centered on the visibility boundary. Route ≤ 3–5 per ticket; no match → `novel — author fresh`.

| Shape | When it applies |
|---|---|
| `layered-endpoint` | any endpoint — thin **router** (parse/authorize/serialize) → **service** (logic) → **repository** (the only layer that touches the DB session). No DB access in a router or service; no logic in a repository. |
| `jwt-auth-dependency` | a protected route — depend on `get_current_user`; a missing/invalid token **denies** (401), never a dev-open fallback. Enforced at the boundary. |
| `owner-scoped-query-guard` | any read/write on a user-owned resource — scope **every** query by owner, deny-by-default; a non-owner target is 404 (not 403 that leaks existence). |
| `public-vs-authored-visibility` | a resource with a draft/published (or private/public) state — **public reads return only published**; a draft is *absent*, never merely hidden client-side. The blog's core promise. |
| `async-repository` | all DB access — async through the repository layer, **one session per request**; no sync driver in the async path, no session leaked above the repository. |
| `alembic-migration-per-schema-change` | any model change — owes a migration; **no `create_all` in the shipped path** (dev-seed only). |
| `cursor-pagination` | any list that can grow unbounded — stable cursor paging, not offset. |
| `structured-error-envelope` | any failure response — a typed `{status, code, detail}`, never a bare 500 or a leaked stack; the status (404 vs 403) is chosen deliberately. |
| `react-query-data-view` | any view that fetches — data via React Query (fetch + mutation); the view renders **loading · empty · error** states, not just the happy path. |
| `mui-themed-component` | any rendered component — built from **MUI + theme tokens**; no raw hex, no magic px, no ad-hoc element where an MUI one exists. The styling-discipline shape. |
| `write-through-audit-log` | any state mutation or denied access — emit a structured **log event** (a stable code) as it lands, so the logs grader can prove the handler ran / the denial fired. |

*(Add shapes as real builds surface them; flag `novel` tickets for promotion once they stabilize.)*

## Tiering signals (what each rubric signal means here)

- **proven pattern** — a catalog hook above applies (not `novel`).
- **verifiable without a human in the loop** — an automated test asserts the criterion: **integration** (real request, real Postgres) or **e2e** (Playwright) against the dev stack. The bar is "a test, not a person, confirms it" — and for a UI ticket, an e2e that checks the **negative** (the withheld thing is absent), not just a 200.
- **risk boundary** — touches **auth, the visibility/ownership boundary (draft→public), an external contract, or the deploy topology**. The visibility boundary is *the* boundary in this profile.
- **out-of-repo dependency** — needs a change outside this codebase you don't control (DNS, a secret, a managed service).
- **spec-complete** — acceptance criterion present + a surface spec exists for any view/endpoint group in scope + a UI state list for any new view.

→ all-pass 🟢 · any-miss 🟡 · risk-boundary or out-of-repo dependency 🔴. Anything crossing the draft→public visibility boundary is **human-only until the visibility test exists** (mirrors isolation in `generic-saas`).

## Grader bar (consumed by `plan-completeness`)

- **`coverage_means`** — every functionality **and every view** in `functional-analysis.md` maps to ≥ 1 ticket whose acceptance criterion, if it passes, delivers it. Visibility is a functionality: it needs its own ticket, not a clause.
- **`verifiable_means`** — an automated test asserts the acceptance criterion. "Handle auth properly" / "hide drafts" fail the bar; a concrete assertion (status code, a row that must/mustn't serialize, a DOM node that must/mustn't render for an anonymous session) passes.
- **well-formed bar:** each ticket carries a test-assertable criterion + a catalog hook (or explicit `novel`) + wired `depends-on`; the backlog carries a cycle-free build order with the critical path called out. The **deploy/infra ticket** is on the path, not an afterthought.

## External tracker sync (optional)

The canonical backlog is `docs/backlog.md`. Mirroring rows to an external tracker (Jira / Linear / GitHub Issues) is an **optional profile add-on**, gated on the driver's OK (shared-tracker writes are outward-facing). The pipeline mechanism is tracker-agnostic; the doc is the source of truth.
