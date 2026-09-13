# roselabs-blog — Current State

> Where things actually are **now**. The first doc a fresh agent reads to orient.
> Memory, not documentation — kept current every ticket. Pulled from `doc-patterns/living-docs/current-state.md`.

> **Profile:** `saas-web` (`.pipeline-profile`). `has_ui: true`, `deploys: true` — the browser check and
> the infra check are live; the smoke row is covered by infra.

## What's built

- **Skeleton + async DB + migrations (T1)** — FastAPI, layered `api → services → repositories`; async
  SQLAlchemy + asyncpg; Alembic chain `0001`–`0005` applies from an empty database (asserted by
  `test_migration.py`); no `create_all` in the app path. `GET /health` → 200.
- **Auth (T2)** — `POST /auth/login` (argon2, generic 401 — no email oracle), `GET /auth/me`,
  `get_current_user` / `get_current_admin` dependencies; HS256 JWT, 1 h TTL, no refresh token;
  `AUTH_DENIED{reason}` on the trace.
- **Invitations (T3)** — admin `POST /invites` (7-day token; the email is logged in dev, Resend is not
  wired), `POST /invites/accept` creates the author and logs them in; expired / used / bad token → 400;
  admin `GET /authors`.
- **Posts (T4, T5)** — owner-scoped create / edit / delete / `GET /posts/mine`; publish / unpublish with
  `published_at` on first publish; non-owner id → 404 (no existence oracle); admin override; unique slugs
  (`core/slug.py`). DB access confined to the repository layer (special-lint clean).
- **Core promise (T6)** — public read paths return only published posts; a draft slug → 404 +
  `DRAFT_ACCESS_DENIED{post,requester}`; an adversarial probe over slug · list · pagination found no leak
  (`test_public_visibility.py`). The manual stand-in for the N-vote.
- **Public read (T7)** — `GET /posts` cursor-paginated on `published_at`, newest first, `?tag=` filter;
  `GET /posts/{slug}`.
- **Tags (T8)** — freeform, slugified, reused by slug; `post_tags` M2M (migration `0004`).
- **Comments (T9, T10)** — anonymous `POST /posts/{slug}/comments` → pending, stored and rendered as
  plain text (a `<script>` body is inert — asserted); moderation `GET /pending`, `approve`, `hide`
  (owner or admin; non-owner → 404; `COMMENT_MODERATION_DENIED` on the trace); only `approved` comments
  serialize publicly.
- **RSS (T11)** — `GET /rss`, RSS 2.0, published only; XML-parse asserted.
- **Web (T12–T16)** — Vite + React 18 + TS + MUI with the roselabs field-notes theme (no raw hex in
  `web/src`); React Query data layer; loading / empty / error states per view. Pages: post list, post
  detail (article body in `<iframe sandbox="">`, decision 0001; approved comments; comment form), login,
  accept-invite, dashboard (own posts, publish / unpublish), editor, moderation, admin authors.
  `ProtectedRoute` redirects unauthenticated users; role-aware nav.
- **Infra (T17, partial)** — `infra/Dockerfile.api` (uv → uvicorn; `entrypoint.sh` runs
  `alembic upgrade head` on boot), `infra/Dockerfile.web` (pnpm build → Caddy serving the SPA and
  proxying `/api` to the api service), `docker-compose.yml` (`db · api · web`, healthchecks, named volume).
  `just up` brings the blog up at `:8080`. The infra check passed: images build, stack healthy on a fresh
  volume, migrations from empty, `/health` + web root through Caddy.

**Tests:** `api/tests/` (pytest against a testcontainers Postgres) and 7 Playwright e2e tests in
`web/e2e/` (visibility · authoring · comments · invites), run against the live Compose stack. All green
at the last gate (2026-08-23).

## What's in flight

- Nothing. No ticket is open in this tree.

## Known gaps / not-yet-built

Checks the `saas-web` profile **declares** that this example has **not wired** (each is a backlog row):
- **a11y** — no `axe-core` run in the e2e beat; the `axe clean` clause of T13–T16 was not asserted.
- **visual-regression** — no screenshot baselines.
- **codemod-check** — the profile mandates `require_auth_dep.py --check api/app/api`; this example ships no
  `codemods/` directory. Protected routes carry `get_current_user` by hand, unverified by a script.
- **security · coverage · deps** rows are declared in the profile's `check-commands.md` but the example's
  `justfile` runs only `ruff + pytest` (`gate-api`) and `tsc + eslint + vitest` (`gate-web`). They have to
  be run by hand.

Product gaps:
- **Deploy (M7)** — no TLS, no `blog.roselabs.io`, no VPS; Compose has three services (Caddy lives inside
  the web image, not as the fourth service the system overview drew). `RESEND_API_KEY` is read from the
  environment but nothing sends email.
- **Author draft preview** — the editor has no preview route (open question, still `[open]`).
- **Comment abuse** — no rate limit, no honeypot; the pending queue can be flooded.
- **JWT_SECRET has a default** — `core/config.py` and `docker-compose.yml` fall back to
  `dev-insecure-change-me…` when the variable is unset. The profile's *auth fails closed* convention says
  a missing key should deny; see `assumptions.md`.
- **Cold rebuild** — this example was built in the same session as its profile and has **not** been
  through `COLD-REBUILD.md`; `saas-web` is unproven from the profile alone.
- **`docs/surfaces/`** — the profile's living-docs set lists per-surface specs; this build wrote
  `ui-sketches.md` + `system-overview.md` and no `surfaces/` directory.

## How to run it

- Stack: `just up` (build + start `api · db · web`), `just seed` (demo author + posts, once), open
  `http://localhost:8080`; `just down` stops and drops the volume. Demo login: see `README.md`.
- Backend gate: `just gate-api` (needs Docker for testcontainers).
- Frontend gate: `just gate-web`.
- Browser check: `pnpm --dir web e2e` against the running stack.
- Infra check by hand: `just down && just up` then `curl -sf localhost:8080/api/health` and
  `curl -sf localhost:8080/ | head -1`.
