# multi-tenant-isolation

A multi-tenant SaaS **projects API** built with the `generic-saas` profile. The hard-done promise:
**no cross-tenant leak on any verb** — a caller of workspace A can never read, list, patch, or delete
workspace B's projects, and a cross-tenant id is indistinguishable from a nonexistent one (404).

Built through the pro-code pipeline: Frame → Plan → Implement, each handoff gated. See `docs/` for the
living spec (`functional-analysis`, `system-overview`, `surfaces/projects`) and the build's memory
(`current-state`, `backlog`, `decisions/`, `assumptions`).

## The isolation guarantee

- **Deny by default at the store** — every query is scoped by `workspace_id`; a foreign id returns nothing.
- **Scope before role** — a cross-tenant delete 404s before the admin gate runs, so 403 never leaks existence (`decisions/0002`).
- **Proven from the trace** — every denial emits `CROSS_TENANT_DENIED{workspace,target}`; the logs grader asserts it fired.
- **Guarded against drift** — `codemods/require_caller_dep.py` enforces `Depends(get_caller)` on every route.

## Run it

1. **Set up the environment**
   ```sh
   poetry install
   export PROJECTS_JWT_SECRET="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
   ```
2. **Run the gate** (this profile ships no task-runner — the graders run via `poetry run`)
   ```sh
   poetry run ruff check app tests codemods
   poetry run pytest --cov=app --cov-report=term-missing
   python3 ../../graders/checks/doctrine_lint.py app tests
   python3 ../../graders/checks/doctrine_lint.py app --forbid 'print\(@@use LOG' --forbid 'except\s*:@@no bare except'
   python3 codemods/require_caller_dep.py --check app/main.py
   poetry run bandit -q -r app && poetry run detect-secrets scan app tests
   poetry export --only main --without-hashes | poetry run pip-audit -r /dev/stdin
   ```
3. **Launch**
   ```sh
   poetry run uvicorn app.main:app --port 8000
   ```

Mint a token to exercise it (same secret as the server):
```sh
python3 -c "import jwt,os; print(jwt.encode({'workspace_id':'A','role':'admin','sub':'u1'}, os.environ['PROJECTS_JWT_SECRET'], algorithm='HS256'))"
```
```sh
curl -H "Authorization: Bearer $TOKEN" localhost:8000/projects
```

## Layout

```
app/        the service — auth · store (scoped) · main (routes) · errors · log · config
codemods/   require_caller_dep.py — boundary-dependency enforcement across handlers
tests/      integration tests per endpoint + the isolation + logs graders
docs/       the living spec + build memory
```
