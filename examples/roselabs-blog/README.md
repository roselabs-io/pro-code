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
- **`docs/`** — the Frame + Plan artifacts (functional-analysis · ui-sketches · system-overview) and the living docs (current-state · backlog · assumptions · open-questions · decisions).

## Run it

Needs Docker. From this directory:

```sh
just up      # build + start api · db · web
just seed    # add a demo author + sample posts (once)
open http://localhost:8080
```

The demo admin is `demo@roselabs.io` / `demo-password-please-change`. Stop with `just down`.

## Configuration

The api reads its settings from environment variables only (`api/app/core/config.py`); it reads no
`.env` file. Names are case-insensitive.

| Variable | Default |
|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://blog:blog@localhost:5432/blog` |
| `JWT_SECRET` | `dev-insecure-change-me-min-32-bytes-long` |
| `JWT_ALG` | `HS256` |
| `ACCESS_TOKEN_TTL_SECONDS` | `3600` |
| `SITE_URL` | `http://localhost:8080` |

`infra/docker-compose.yml` sets `DATABASE_URL` for the `api` service and passes `JWT_SECRET` from the
shell, with the default above when it is unset.

## Gate it

```sh
just gate-api   # ruff + pytest (spins a real Postgres via testcontainers)
just gate-web   # tsc + eslint + vitest
```

Backend tests need Docker (testcontainers). The frontend end-to-end (browser) check runs against the
running Compose stack.
