# Profile — `generic-saas` · check-commands

The deterministic graders read this file directly — the **active-profile handshake** (the pipeline resolves
the active profile's `check-commands.md`, never a hardcoded path). Split out of `implement-profile.md` so a
grader reads one file for its command.

## Commands *(shell — run first, short-circuit)*

| grader | command | rule / threshold |
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

## Other graders wired

- **logs** — run: replays a request and asserts `CROSS_TENANT_DENIED{workspace,target}` fired (isolation
  proven from the *trace*, not the 404 alone). Events per `doc-patterns/harness/log-taxonomy.md`.

## Declared n/a *(not skipped — why)*

- **schema-validation** — pydantic validates request/response at runtime (a bad body → 422; the integration
  tests assert it), so there's no separate schema command.
- **browser / e2e** — API-only (`has_ui: false`), no rendered surface.

## Allowlists + paths

- **security allowlist** — none (the LOG module's own `print` is a `doctrine: allow`, handled by the
  comment doctrine, not here).
- **license allowlist** — MIT · BSD-2/3 · Apache-2.0 · ISC · PSF.
- **manifest paths** — `pyproject.toml` + `poetry.lock`.
- **coverage exclude** — none coverable-excluded by default; any generated code excluded via `[tool.coverage]`.
