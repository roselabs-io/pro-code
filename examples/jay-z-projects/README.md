# jay-z-projects

The same multi-tenant **projects API** as `multi-tenant-isolation` — hard-done = **no cross-tenant leak
on any verb** — but built under the **`generic-saas` + `personal/jay-z` overlay**. Every comment and
docstring carries Jay-Z's voice **while staying comment-doctrine-clean**: still one line, still stating
what the code *is*, no why-not / history / ticket-ref. Swagger in the phrasing, never in the length or the
content.

This is the additive-only overlay made concrete: the voice can only hold the code to *more* (voice **and**
the doctrine), never less. GATE-0 warns that the composed fuzzy set is 4 (feature · drift · docs-currency ·
**jay-z-voice**) — the personal opt-in's justified +1 — and does not block.

## The isolation guarantee (identical to #1)

- **Deny by default at the store** — every query scoped by `workspace_id`; a foreign id returns nothing.
- **Scope before role** — a cross-tenant delete 404s before the admin gate, so 403 never leaks existence (`decisions/0002`).
- **Proven from the trace** — every denial emits `CROSS_TENANT_DENIED{workspace,target}`; the logs grader asserts it.
- **Guarded against drift** — `codemods/require_caller_dep.py` enforces `Depends(get_caller)` on every route.

## The voice (a taste of what the overlay demands)

```python
# No token, no entry — pull the caller straight off the bearer, or deny.
def get_caller(...): ...

# Hand over the project only if it's yours — else None, deny by default.
def get(self, workspace_id, project_id): ...
```
Both carry the swagger *and* pass `doctrine_lint.py` — one line, stating what the code is.

## Run it

1. **Set up the environment**
   ```sh
   poetry install
   export PROJECTS_JWT_SECRET="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
   ```
2. **Run the gate** (no task-runner in this profile — the graders run via `poetry run`)
   ```sh
   poetry run ruff check app tests codemods
   poetry run pytest --cov=app --cov-report=term-missing
   python3 ../../graders/checks/doctrine_lint.py app tests
   python3 ../../graders/checks/doctrine_lint.py app --forbid 'print\(@@use LOG' --forbid 'except\s*:@@no bare except'
   python3 codemods/require_caller_dep.py --check app/main.py
   poetry run bandit -q -r app && poetry run detect-secrets scan app tests
   poetry export --only main --without-hashes | poetry run pip-audit -r /dev/stdin
   ```
   The `jay-z-voice` grader is a fuzzy (LLM) grader — run by the verification loop, not a shell command.
3. **Launch**
   ```sh
   poetry run uvicorn app.main:app --port 8000
   ```

## Layout

```
app/        the service — same logic as #1, every comment re-voiced (doctrine-clean)
codemods/   require_caller_dep.py — boundary-dependency enforcement across handlers
tests/      integration tests per endpoint + the isolation + logs graders
docs/       the living spec + build memory
```
