---
consumed_by: [orchestrator, build]
canonical_for: `local-app` check rows: command, threshold, n/a reasons
profile: local-app
---

# Profile — `local-app` · check-commands

The checks read this file directly — the active-profile handshake. Row names and order:
[`../../checks/README.md`](../../checks/README.md#the-deterministic-tier-in-order).

## Commands *(must — one row per check, in run order)*

| check | command | rule / threshold |
|---|---|---|
| lint | `ruff check src tests` | no violations |
| type-check | `mypy src/` | advisory — not a gate step |
| doctrine-lint | `doctrine_lint.py src tests --forbid 'Anthropic\(@@the remote model is called from chain/llm.py only' --allow-path src/*/chain/llm.py` | comment-doctrine + test-posture floor + one-egress |
| codemod-check | n/a — no codemod; `ruff --fix && ruff format` as codemod-lite | — |
| security | `bandit -q -r src` + `detect-secrets scan` | no high-severity finding · **secrets = hard fail** (an API key in the repo is the domain's worst case) |
| tests | `pytest -m "not browser and not slow and not api"` (fast) · `pytest -m slow` (model-loading fixtures) · `pytest -m api` (skipped without a key) | zero failures, this session |
| coverage | `pytest -m "not browser" --cov=src --cov-report=term-missing` | changed-line ≥ 80 % |
| deps | `uv export --no-dev --no-hashes \| pip-audit -r -` | critical vuln = hard fail · lockfile consistent |
| schema-validation | n/a — every model call is schema-constrained at the call; a failed parse is a test failure | — |
| logs | `pytest tests/test_trace.py` — runs one synthetic input through the chain and asserts the trace holds redacted text, the stages' outputs and decisions, and **zero answer-key spans** in any file under the run's folder | the trace is complete and clean |
| smoke | launch `just app --headless` · probe the bridge with one `ping` · stop | the process starts, answers, stops |
| browser | `pytest -m browser` — Playwright against the window's page; `visual_invariant`: the placeholder pane shows no answer-key span, and *Rédiger* is disabled until the pane has rendered | the boundary is visible before egress |
| infra | n/a — `deploys: false` | — |

## Allowlists + paths *(may)*

- **security allowlist** — none.
- **license allowlist** — MIT · BSD-2/3 · Apache-2.0 · ISC · PSF · MPL-2.0.
- **manifest paths** — `pyproject.toml` + `uv.lock`.
- **coverage exclude** — `src/*/ui/static/`, `explore/` (learning files, not product code).

## Declared n/a *(not skipped — why)*

- **codemod** — drift is caught by the drift grader and the one-egress forbid; no bulk transform.
- **schema-validation** — constrained at the call; there is no separate contract document.
- **infra** — a single local process; nothing to build or boot beyond the smoke row.
