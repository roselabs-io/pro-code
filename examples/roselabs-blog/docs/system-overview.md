# roselabs-blog — System Overview

> The engineering shape Implement builds against: layers, the two invariants, the stack, and where the
> graders bite. Pulled from `doc-patterns/specs/system-overview.md`; filled per the `saas-web` profile.

## Shape

A full-stack app, two deployables behind one reverse proxy:

```
              ┌───────── Caddy (TLS, blog.roselabs.io) ─────────┐
              │                                                  │
     ┌────────┴────────┐                          ┌──────────────┴───────┐
     │  web (React/MUI)│  ──── /api ────────────▶ │  api (FastAPI async) │
     │  Vite build     │      React Query/axios   │  routers → services  │
     └─────────────────┘                          │   → repositories     │
                                                   └──────────┬───────────┘
                                                              │ asyncpg
                                                       ┌──────┴───────┐
                                                       │  Postgres 16 │
                                                       └──────────────┘
```

## Backend layers (strict)

- **`app/api/`** routers — parse · authorize (`get_current_user`) · serialize. No DB, no business logic.
- **`app/services/`** — the logic (publish rules, visibility filtering, moderation).
- **`app/repositories/`** — the **only** layer holding an `AsyncSession`; owner-scoped queries live here.
- **`app/models/`** (SQLAlchemy) · **`app/schemas/`** (pydantic) · **`app/core/`** (config · DB session · JWT security · logging).

Enforced by the special-lints: no `AsyncSession` above the repository; no `create_all` in the app path; no `print` (use `LOG`).

## The two invariants (the whole point)

1. **Post visibility + ownership** — public reads return only `published`; a draft is 404 (indistinguishable from unknown); an author touches only their own posts. Enforced in the **repository** (deny-by-default, owner-scoped), proven by integration + e2e + N-vote. `DRAFT_ACCESS_DENIED` on the trace.
2. **Comment moderation** — a comment is `pending` until an owner/admin approves; only `approved` serializes publicly. The second visibility boundary.

Both live **server-side**; the React app is convenience only and must never be the thing that hides a draft.

## Content rendering (decision 0001)

- **Article body** — trusted rich HTML, rendered in a **sandboxed iframe** (`srcdoc`, no `allow-scripts`): full CSS/SVG isolation, no script, no style bleed with the app's MUI/CSS-in-JS.
- **Comment body** — untrusted, stored/rendered as **plain text**; no HTML interpreted.

## Frontend

React + TS + Vite + MUI; data via React Query + axios; all styling through the **roselabs MUI theme/tokens** (the styling discipline — no raw hex/px). Views per `ui-sketches.md`; each fetching view renders loading · empty · error.

## Where the graders bite

- **deterministic:** ruff/eslint · mypy/tsc (advisory) · doctrine-lint + special-lints · **pytest integration on a testcontainers Postgres** · vitest · bandit/detect-secrets/audits · coverage.
- **logs:** `DRAFT_ACCESS_DENIED`, `AUTH_DENIED` fired on the trace.
- **browser (Playwright):** the visual invariant — a draft never in the DOM for anon; author-only controls never render for a reader; `axe` clean; visual-regression baselines.
- **infra:** `docker compose build` + up + smoke + migrate-from-empty (`deploys: true`).
- **fuzzy (~3, fresh sub-agents):** feature · drift (incl. styling discipline + undeclared-choice) · docs-currency; **adversarial N-vote** on T6/T10.

## Deploy topology (single VPS)

Docker Compose: `api` (multi-stage Python) · `web` (multi-stage node build → static, served by Caddy or a tiny server) · `postgres` (named volume) · `caddy` (auto-TLS). Secrets via `.env` (git-ignored; `.env.example` committed; `RESEND_API_KEY` wired at M7). Migrations run on release, never `create_all`.
