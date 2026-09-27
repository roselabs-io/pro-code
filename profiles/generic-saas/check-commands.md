---
consumed_by: [orchestrator, build]
canonical_for: `generic-saas` check rows: command, threshold, n/a reasons
profile: generic-saas
---

# Profile — `generic-saas` · check-commands

The checks read this file directly — the **active-profile handshake** (the pipeline resolves
the active profile's `check-commands.md` per [`../CONTRACT.md#active-profile-resolution`](../CONTRACT.md#active-profile-resolution),
never a hardcoded path). Split out of `implement-profile.md` so a check reads one file for its command.
Row names + order: [`../../checks/README.md`](../../checks/README.md#the-deterministic-tier-in-order).

## Commands *(shell — run first, short-circuit)*

| check | command | rule / threshold |
|---|---|---|
| lint | `ruff check app tests codemods` | no lint errors |
| tests | `pytest` | zero failures, this session |
| type-check | `mypy app/` | advisory — author-aid, **not** a gate step this slice |
| doctrine-lint | `doctrine_lint.py app tests` | comment-doctrine + test-posture floor |
| special-lint | `doctrine_lint.py app --forbid 'print\(@@use LOG' --forbid 'except\s*:@@no bare except'` | no `print` in app code · no bare `except` |
| codemod-check | `codemods/require_caller_dep.py --check app/main.py` | every route carries the boundary dependency |
| security | `bandit -q -r app` + `detect-secrets scan` | no high-severity SAST finding · **secrets = hard fail** |
| coverage | `pytest --cov=app --cov-report=term-missing` | changed-line ≥ 80% |
| deps | `poetry export --only main --without-hashes \| pip-audit -r -` | **critical vuln = hard fail** · lockfile consistent · audits the **shipped tree**, not the dev/security tooling's transitives |
| smoke | launch `poetry run uvicorn app.main:app --port 8000 &` · probe `curl -sf localhost:8000/openapi.json` → 200 · stop `kill %1` | the process boots and answers (`deploys: false` → this is the runtime floor) |

## Other checks wired

- **logs** — run: replays a request and asserts `CROSS_TENANT_DENIED{workspace,target}` fired (isolation
  proven from the *trace*, not the 404 alone). Events per `doc-patterns/harness/log-taxonomy.md`.

## Declared n/a *(not skipped — why)*

- **schema-validation** — pydantic validates request/response at runtime (a bad body → 422; the integration
  tests assert it), so there's no separate schema command.
- **browser / e2e** — API-only (`has_ui: false`), no rendered surface.
- **infra** — `deploys: false`; nothing to build and boot as an image. The **smoke** row above is the boot floor.

## Allowlists + paths

- **security allowlist** — none (the LOG module's own `print` is a `doctrine: allow`, handled by the
  comment doctrine, not here).
- **license allowlist** — MIT · BSD-2/3 · Apache-2.0 · ISC · PSF.
- **manifest paths** — `pyproject.toml` + `poetry.lock`.
- **coverage exclude** — none coverable-excluded by default; any generated code excluded via `[tool.coverage]`.
