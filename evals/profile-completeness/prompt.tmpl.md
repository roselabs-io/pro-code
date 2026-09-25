---
name: profile-completeness
description: "GATE 0 on a project whose stack matches one shipped profile."
tags: [grader, gate-0]
max_turns: 6
allowed_tools: [Read]
append_system_prompt: |
{{RUBRIC}}
---

You are the **profile-completeness** grader, GATE 0 of a build pipeline. You are a fresh
sub-agent: you did not write the project or the profiles described below. Your rubric is in your
system prompt. Where your own instincts and the rubric disagree, the rubric wins.

## Context

The pipeline is about to run on the project below. Everything you can know about the project,
the runner, and the pipeline's profile directory is in this message; there is nothing else to
read.

### The project root

`ls -a` of the directory the pipeline runs in:

```
.
..
.dockerignore
.git
.gitignore
README.md
api
docs
infra
justfile
web
```

The opening of its `README.md`:

```
# acme-notes

A web app for shared notes. FastAPI (async) + React/MUI + async Postgres, shipped as a
Docker Compose stack (api · db · web) behind Caddy.

## Shape

- `api/` — FastAPI, layered routers → services → repositories, async SQLAlchemy, Alembic.
- `web/` — React + TypeScript + Vite + MUI.
- `infra/` — Dockerfiles + Compose, Caddy serving the SPA and proxying /api.
- `docs/` — the spec and the living docs.
```

`api/` holds `pyproject.toml`, `uv.lock`, `alembic/`, `app/`, `tests/`. `web/` holds
`package.json`, `pnpm-lock.yaml`, `src/`, `e2e/`, `playwright.config.ts`. `infra/` holds
`docker-compose.yml`, `Dockerfile.api`, `Dockerfile.web`, `Caddyfile`.

### The runner

`env` in the runner, filtered to the variables that could concern a build pipeline:

```
HOME=/home/runner
PATH=/usr/local/bin:/usr/bin:/bin
SHELL=/bin/bash
CI=true
UV_CACHE_DIR=/home/runner/.cache/uv
PNPM_HOME=/home/runner/.local/share/pnpm
```

### The pipeline's profiles directory

```
profiles/
  CONTRACT.md
  README.md
  _skeleton/        check-commands.md  frame-profile.md  implement-profile.md  plan-profile.md
                    personal-profile.md  grader.md
  edge-telemetry/   check-commands.md  frame-profile.md  implement-profile.md  plan-profile.md
  generic-saas/     check-commands.md  frame-profile.md  implement-profile.md  plan-profile.md
  saas-web/         check-commands.md  frame-profile.md  implement-profile.md  plan-profile.md
  personal/
    README.md
    jay-z/          personal-profile.md  graders/jay-z-voice.md
```

The flag lines from each domain profile's `frame-profile.md`:

```
edge-telemetry:  has_ui: true   deploys: false
generic-saas:    has_ui: false  deploys: false
saas-web:        has_ui: true   deploys: true
```

A grep for `{TODO}` across the three domain profiles returns nothing. Every path the three
profiles reference exists. Each `check-commands.md` has every row of the deterministic tier
filled or declared n/a with a reason.

## How to answer

Run GATE 0 on this project. Say what you find, and what has to happen before Frame may run, if
anything.

Then end your reply with exactly these two lines and nothing after them:

```
VERDICT gate0: <pass|fail|unknown>
GRADED profile: <domain name|none>
```

- `pass` — the profile set is admissible and Frame may run now.
- `fail` — Frame may not run; your prose names what must change first.
- `unknown` — you could not reach a verdict.
- `GRADED profile` — the domain profile whose contents you assessed for admissibility, or
  `none` if you assessed none.
