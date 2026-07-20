# Profile — `saas-web` · Implement

Domain: a **full-stack web SaaS** — FastAPI (async) + React/TS/MUI + async Postgres, deployed via Docker
Compose. Completes the trio with `frame-profile.md` and `plan-profile.md`.

The hard-done requirement — **no draft or unpublished resource is readable by a public request** — is
proven the way isolation was in `generic-saas`: by an integration test on the real query path **and** an
e2e test on the rendered surface, then held under the adversarial N-vote. The grader, not confidence,
certifies it.

> **This profile mandates** (its opinionated subset — the union of the SaaS *and* UI opinions, plus deploy): a **codemod** (every protected router depends on `get_current_user`), the **logs grader**, an **integration test per endpoint against a real Postgres**, the **browser grader + an e2e test**, an **a11y check** (`axe`), **visual-regression snapshots**, and the **infra grader** (`deploys: true`). The `no-print` / `no-bare-except` / `no-raw-color` / `no-create-all-in-app` special-lints.
> **It skips**: nothing agnostic — it's the fullest profile. `schema-validation` is declared n/a (pydantic + TS types validate at the edges).

## Stack + layout

- **Backend:** Python + **FastAPI** (ASGI, **async**); served with `uvicorn`. Layered: `app/api/` (routers, thin) → `app/services/` (logic) → `app/repositories/` (the only layer touching the DB session) → `app/models/` (SQLAlchemy) + `app/schemas/` (pydantic). `app/core/` holds config, the DB session factory, and security (JWT).
- **DB:** **Postgres 16**, **async SQLAlchemy 2.x + asyncpg**, **Alembic** migrations. One `AsyncSession` per request (a FastAPI dependency); **no `create_all` in the shipped path** — migrations only (dev-seed may create_all).
- **Auth:** **JWT bearer via FastAPI `Depends`** (`get_current_user`); **argon2** password hashing. Auth **fails closed** — a missing/invalid token or signing key denies; never a dev-open fallback in the gated path.
- **Frontend:** **React + TypeScript + Vite + MUI**; data via **React Query + axios**; **eslint + prettier**; **vitest** (unit) + **Playwright** (e2e). All styling through the **MUI theme + tokens** (`web/src/theme/`).
- **Env / runner:** **uv** (`uv sync`) for the backend + **pnpm** for the frontend, coordinated by a **`justfile`** (`just gate`, `just up`, `just e2e`) whose recipes call `uv run` / `pnpm`.
- **Python:** ≥ 3.12. **Node:** ≥ 20.
- **Lint / format:** `ruff` (backend — `line-length = 90`, rules `E, F, I, B`; `extend-immutable-calls` for FastAPI DI so `B008` doesn't fire on route-default `Depends()`); `eslint` + `prettier` (frontend).
- **Tests:** `pytest` with a **real Postgres** via **testcontainers** (a container per session — the integration tests hit the real async query path, not a mock) and a `browser` marker for the Playwright e2e (`-m "not browser"` unit/integration, `-m browser` e2e). Playwright needs a one-time `playwright install chromium`.
- **Infra:** Docker (multi-stage images for `api` and `web`) + **docker-compose** (`api · web · postgres · caddy`); **Caddy** for reverse-proxy + auto-TLS. Secrets/config via `.env` (git-ignored; `.env.example` committed).

> These are the profile's **declared choice-points** — fixed here so they're not silent. Any build choice *not* covered here (or by the Conventions below) goes in `docs/assumptions.md` with a disposition.

## Deterministic checks

Commands, thresholds, and allowlists live in this profile's [`check-commands.md`](check-commands.md) — the file the graders read directly (the active-profile handshake). This profile **runs**: lint (backend + frontend) · tests (integration on real Postgres + unit + e2e) · type-check (advisory: `mypy` + `tsc`) · doctrine-lint · special-lint · codemod-check · **security** · **coverage** · **deps** · logs · **browser** · **a11y** · **visual-regression** · **infra**. It declares **schema-validation** *n/a* (pydantic + TS types validate at the edges). See `check-commands.md`.

## Fuzzy rubrics (~3 focused graders — what each points at)

- **feature / spec** → the ticket's acceptance criterion. Does the diff satisfy the assertion end-to-end — including the **negative** (the withheld thing is absent for an anonymous session), not a 200 proxy?
- **pattern / drift** → the design catalog (`plan-profile.md`) hooks + the conventions below, **including the styling discipline**. Was `owner-scoped-query-guard` applied to **every** verb, deny-by-default? Is styling theme-only, no raw hex? Plus the **undeclared-choice lens** (a library/pattern no input specified → `docs/assumptions.md`).
- **docs-currency** → the living-docs set below. Backlog pruned + forward-only, current-state fresh, a decision record for any new decision, open-questions flipped, UI sketches + surfaces current.

## Full-coverage machinery (guides + graders this profile wires)

- **LSP (guide):** `mypy app/` (backend) + `tsc --noEmit` (frontend) — types/refs while authoring. Advisory, not a gate step this slice.
- **Environment + CLIs (guide):** **uv** (`uv sync`) + **pnpm** + a **`justfile`** (`just gate`) whose recipes call `uv run` / `pnpm`. Template: `doc-patterns/harness/justfile`.
- **Codemods (auto-fix arm):** codemod-lite = `ruff check --fix . && ruff format .` + `eslint --fix && prettier -w` every gate; one **libcst** codemod enforcing that **every protected route depends on `get_current_user`** (the boundary convention, across `app/api/`). See the example's `codemods/`.
- **Logs grader:** structured events per `doc-patterns/harness/log-taxonomy.md` — `HANDLER_RAN`, `AUTH_DENIED{reason}`, `DRAFT_ACCESS_DENIED{post,requester}`. The grader replays an anonymous request for a draft and asserts `DRAFT_ACCESS_DENIED` fired (the *no-draft-leak* promise proven from the trace, not the 404 alone).
- **Browser grader (LIVE here):** `has_ui: true`. Playwright drives the running app; **`visual_invariant`: a draft never appears in the DOM for an anonymous session, and an author-only control (edit/delete) never renders for a reader.** The only grader that catches a client rendering withheld content while every API test stays green.
- **Infra grader (LIVE here):** `deploys: true`. `docker compose build` + bring the stack up + a smoke check (the API `/health` is 200, the web root serves, a migration ran) — "it builds and boots" is part of done. See [`../../graders/infra-grader.md`](../../graders/infra-grader.md).

## Doctrines this profile mandates

- **Comment doctrine** (`doc-patterns/doctrines/comment-doctrine.md`) — shared/universal, enforced by `doctrine_lint.py` + the fuzzy drift grader.
- **README doctrine** (`doc-patterns/doctrines/readme-doctrine.md`) — the service README carries a "Run it" section: set up (`uv sync` · `pnpm install`), run `just gate`, launch (`just up`). Checked by the docs-currency grader.
- **Test posture** (`doc-patterns/doctrines/test-posture.md`) — this domain's opinion:
  - **An integration test per endpoint, against a real Postgres** — every route drives the *real* request through the app (async, testcontainers Postgres) and asserts the **effect** (a row changed, a field serialized, a draft *not* returned), not the status. Mocking the DB is a false green.
  - **An e2e test, because there is a frontend** — Playwright drives the running app and asserts the visual invariant *and its negative* (the draft/author-control is absent for the wrong viewer). A UI-bearing profile owes this layer.
  - Per-endpoint the matrix is: **happy · auth-required (401) · validation (422) · not-found (404) · ownership/visibility (a non-owner/anonymous request is withheld)**.
  - Plus the floor: every test asserts; no silent skip; red-green on a fix.

## Special-lint (the domain forbids — `doctrine_lint.py --forbid`)

- **no `print(` in app code** — use the structured `LOG` event log. The log module itself is `doctrine: allow`.
- **no bare `except:`** — catch a specific type.
- **no raw color / magic px in `web/src`** — style through the MUI theme + tokens, not inline hex or hard-coded pixels. The theme file is `doctrine: allow`.
- **no `create_all(` in `app/`** — schema changes ship as Alembic migrations, not runtime table creation (dev-seed scripts are `doctrine: allow`).
- **no DB *operations* (`session.execute/add/get/scalar/delete/flush/commit`) outside `app/repositories/`** — routers/services may *reference* the session type to thread it down, but must never query with it; a query above the repository is a layering breach.

## Conventions (the drift grader's rubric)

- **Layered, strictly** — routers parse/authorize/serialize; services hold logic; repositories own the DB session. No DB in a router/service; no logic in a repository.
- **Async all the way** — no sync DB driver or blocking call in the async request path; one `AsyncSession` per request, not leaked above the repository.
- **Enforce at the boundary, not the client** — authz/visibility checks live server-side; the React app is convenience only and must never be the thing that hides a draft.
- **Auth fails closed** — a missing/invalid signing key or token **denies**; never a fallback to an unsigned/dev-open path. *(The generic-saas cold-run lesson, carried forward.)*
- **Deny-by-default on ownership** — an unscoped query returns nothing; a non-owner target is 404, not a 403 that leaks existence.
- **Migrations, not `create_all`** — every model change owes an Alembic migration; the shipped path never creates tables at runtime.
- **Styling is theme-only** — MUI components + theme tokens; no raw hex, no magic px, responsive, works in light **and** dark; state is not colour-only (a11y). *(The styling discipline — brand-agnostic; the actual theme is example content.)*
- **Errors are typed + tiered** — a permission-denied returns the chosen status (404 for a withheld resource); no bare 500s for expected failures.
- **Views render their states** — every fetching view handles loading · empty · error, not just the happy path.
- **No magic numbers** — limits/TTLs/page-sizes are named config, not literals.
- **Tests live with the ticket** — not "later."
- **Comment doctrine** — state what the code *is*; the why-not / history / ticket-ref belongs in the commit.

## verify_means + false-green traps

- **verify_means:** an **integration test on the real query path (real Postgres)** asserts the API effect, **and** a **Playwright e2e** asserts the rendered behaviour *and its negative*, with fresh output this session — a test, not a person, confirms it. For the deploy dimension, the **infra grader** proves the stack builds and boots.
- **false-green traps** (the `check-passes-but-behaviour-is-broken` class the fuzzy feature grader must probe past):
  - **mock-green ≠ real-green** — a mocked DB that always says yes hides the integration bug; the visibility test must hit the **real** async query path (testcontainers Postgres).
  - **`200 ≠ the handler ran`** — assert the *effect* (a row changed, a draft *absent* from the payload), not the status.
  - **happy-path-only** — an endpoint with no auth-denied / validation / not-found / non-owner case is under-tested; the per-endpoint matrix is the floor.
  - **e2e asserts the positive, not the negative** — a test that a *published* post renders says nothing about whether a **draft leaks**; assert the withheld thing is **absent** for the anonymous session.
  - **client renders what the API withheld** — the API returns only published, but a template/route bug renders a draft or an author-only control to a reader; the browser grader is the only catch.
  - **serialization drops a falsy field** — a `false`/`0`/`""` silently missing looks like "not returned"; assert presence.
  - **no red-green on a fix** — a regression test never seen to fail first proves nothing.

## Living docs (the docs-currency grader's set)

Kept current every ticket — the second artifact:
- `docs/backlog.md` — forward-only (shipped rows deleted; new work added).
- `docs/current-state.md` — what's built now.
- `docs/open-questions.md` — resolved flipped to `[decided]`; new assumptions `[open]`.
- `docs/decisions/NNNN-*.md` — a record per non-obvious call (template: `doc-patterns/living-docs/decision-record.md`).
- `docs/surfaces/<name>.md` + `docs/ui-sketches.md` — updated if reality diverged from Plan's sketch.
- `docs/assumptions.md` — the choices the build made that no input specified, each with a disposition (template: `doc-patterns/living-docs/assumptions.md`).
