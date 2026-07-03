# multi-tenant-isolation

A multi-tenant SaaS **Projects API** (backend only) built through the pro-code pipeline on the
**`generic-saas`** profile. Many workspaces share one deployment; each workspace's data is invisible
to every other. **Hard-done: no cross-tenant leak** — a cross-tenant id is indistinguishable from
not-found, certified by `tests/test_isolation.py`.

- **Stack:** Python 3.12 · FastAPI · PyJWT (HS256) · in-memory store. Env: **poetry** (no task-runner).
- **Isolation:** enforced at the request boundary — `get_caller` resolves the tenant, a
  workspace-scoped store denies by default, a foreign id returns 404 (never 403).

## Layout

```
app/         the service — auth · errors · store · models · routes · log · config
codemods/    require_caller_dep.py — libcst: every route must take the boundary dep
tests/       integration test per endpoint + the isolation certification + logs grader
docs/        the pipeline's output — spec, plan, living docs, assumptions ledger
```

## Run it

```bash
poetry install
```

Gate (deterministic graders, in short-circuit order — this profile ships no task-runner, so the
grader commands are listed explicitly):

```bash
# 0. auto-fix arm (codemod-lite)
poetry run ruff check --fix app tests codemods && poetry run ruff format app tests codemods
# 1. lint
poetry run ruff check app tests codemods
# 2. comment-doctrine + test-posture floor
poetry run python ../../graders/checks/doctrine_lint.py app tests
# 3. special-lint (domain forbids: no print, no bare except)
poetry run python ../../graders/checks/doctrine_lint.py app \
  --forbid 'print\(@@use LOG' --forbid 'except\s*:@@no bare except'
# 4. boundary-dependency codemod check
poetry run python codemods/require_caller_dep.py --check app/main.py
# 5. the verify gate
poetry run pytest -q
# (advisory, author-aid, not a gate step)
poetry run mypy app/
```

Launch:

```bash
poetry run uvicorn app.main:app --port 8000
```

The gate is green: **27 tests**, ruff/doctrine/special-lint/codemod all clean.
