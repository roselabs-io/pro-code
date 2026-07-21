# Profile — `saas-web` · check-commands

The deterministic graders read this file directly — the **active-profile handshake** (the pipeline resolves
the active profile's `check-commands.md`, never a hardcoded path). Split out of `implement-profile.md` so a
grader reads one file for its command.

Backend runs under `uv` (`uv run …`), frontend under `pnpm` (`pnpm --dir web …`); a `justfile` wraps the
common combinations (`just gate`). Paths assume `api/` (backend) and `web/` (frontend).

## Commands *(shell — run first, short-circuit)*

| grader | command | rule / threshold |
|---|---|---|
| lint | `ruff check api` + `pnpm --dir web lint` | no lint errors (backend + frontend) |
| tests | `uv run pytest -m "not browser"` (unit + integration on a testcontainers Postgres) + `pnpm --dir web test` (vitest) + `uv run pytest -m browser` (Playwright e2e) | zero failures, this session |
| type-check | `uv run mypy api/app` + `pnpm --dir web typecheck` (`tsc --noEmit`) | advisory — author-aid, **not** a gate step this slice |
| doctrine-lint | `doctrine_lint.py api tests` | comment-doctrine + test-posture floor |
| special-lint | `doctrine_lint.py api --forbid 'print\(@@use LOG' --forbid 'except\s*:@@no bare except' --forbid 'create_all\(@@ship migrations, not create_all'` · `doctrine_lint.py web/src --forbid '#[0-9a-fA-F]{6}@@style via the theme, not raw hex'` · `doctrine_lint.py api/app/api api/app/services --forbid 'session\.(execute\|add\|get\|scalars?\|delete\|flush\|commit)@@DB access stays in the repository layer'` | no `print` · no bare `except` · no `create_all` in app · no raw hex in web · no DB **ops** above the repository (routers/services may reference the session type to thread it, never query with it) |
| codemod-check | `uv run codemods/require_auth_dep.py --check api/app/api` | every protected route carries the `get_current_user` dependency |
| security | `uv run bandit -q -r api/app` + `detect-secrets scan` + `pnpm --dir web audit --audit-level high` | no high-severity SAST finding · **secrets = hard fail** · no high frontend advisory |
| coverage | `uv run pytest -m "not browser" --cov=api/app --cov-report=term-missing` + `pnpm --dir web test -- --coverage` | changed-line ≥ 80% (backend); frontend components exercised by unit + e2e |
| deps | `uv export --no-dev --no-hashes \| pip-audit -r -` + `pnpm --dir web audit --prod` | **critical vuln = hard fail** · lockfiles consistent · audits the **shipped tree**, not dev/CI tooling |

## Other graders wired

- **logs** — run: replays an anonymous request for a draft and asserts `DRAFT_ACCESS_DENIED{post,requester}` fired (the *no-draft-leak* promise proven from the trace, not the 404 alone). Events: `HANDLER_RAN`, `AUTH_DENIED{reason}`, `DRAFT_ACCESS_DENIED{post,requester}`. Per `doc-patterns/harness/log-taxonomy.md`.
- **browser / e2e** — run (**live**, `has_ui: true`): `uv run pytest -m browser` / `pnpm --dir web e2e` — Playwright drives the running app; `visual_invariant` — a draft never renders in the DOM for an anonymous session; an author-only control (edit/delete) never renders for a reader.
- **a11y** — run (in the Playwright beat): `axe-core` against each rendered view; no serious/critical violations; state is not colour-only; interactive elements are keyboard-reachable and labelled.
- **visual-regression** — run: Playwright screenshots vs committed baselines (`web/tests/e2e/__snapshots__/`); an un-reviewed visual diff is a finding. Baselines are updated deliberately (a decision), never blind-accepted.
- **infra** — run (**live**, `deploys: true`): `docker compose -f infra/docker-compose.yml build` then bring up + smoke — `GET /health` is 200, the web root serves HTML, a migration ran cleanly on a fresh volume. See [`../../graders/infra-grader.md`](../../graders/infra-grader.md).

## Declared n/a *(not skipped — why)*

- **schema-validation** — pydantic validates request/response and TS types validate the client at the edges (a bad body → 422; the integration tests assert it), so there's no separate schema command.

## Allowlists + paths

- **security allowlist** — none (the `LOG` module's own `print`, the theme file's colors, and dev-seed `create_all` are `doctrine: allow`, handled by the comment doctrine / special-lint exemptions, not here).
- **license allowlist** — MIT · BSD-2/3 · Apache-2.0 · ISC · PSF · (frontend) MIT · ISC · Apache-2.0.
- **manifest paths** — backend `api/pyproject.toml` + `api/uv.lock`; frontend `web/package.json` + `web/pnpm-lock.yaml`.
- **coverage exclude** — Alembic migration scripts, generated API client, and the MUI theme tokens (exercised by the browser + visual-regression graders, not unit coverage).
