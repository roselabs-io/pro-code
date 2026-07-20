# roselabs-blog

Example #3 in [pro-code](../../README.md) — built with the **`saas-web`** profile. A full-stack web
SaaS: **FastAPI (async) + React/MUI + async Postgres**, deployed as a Docker Compose stack.

The hard-done — the profile's core promise — is **no draft or unpublished post is readable by a public
request**, certified by an integration test on the real query path + an adversarial probe + a
`DRAFT_ACCESS_DENIED` audit trace (not by author confidence).

## Shape

- **`api/`** — FastAPI, layered `routers → services → repositories`, async SQLAlchemy + asyncpg, Alembic.
  JWT auth (argon2), owner-scoped posts, public read paths that surface only published content.
- **`web/`** — React + TS + Vite + MUI, the roselabs "field-notes" theme. Article bodies render in a
  **sandboxed iframe** (decision 0001) — full CSS/SVG isolation.
- **`infra/`** — Dockerfiles + Compose (`api · db · web`), Caddy serving the SPA and proxying `/api`.
- **`docs/`** — the Frame + Plan artifacts (functional-analysis · ui-sketches · backlog · decisions).

## Run it

Needs Docker. From this directory:

```sh
just up      # build + start api · db · web
just seed    # add a demo author + sample posts (once)
open http://localhost:8080
```

The demo admin is `demo@roselabs.io` / `demo-password-please-change`. Stop with `just down`.

## Gate it

```sh
just gate-api   # ruff + pytest (spins a real Postgres via testcontainers)
just gate-web   # tsc + eslint + vitest
```

Backend tests need Docker (testcontainers). The frontend end-to-end (browser) grader runs against the
running Compose stack.
