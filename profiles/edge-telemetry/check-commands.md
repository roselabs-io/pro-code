# Profile — `edge-telemetry` · check-commands

The deterministic graders read this file directly — the **active-profile handshake** (the pipeline resolves
the active profile's `check-commands.md`, never a hardcoded path). Split out of `implement-profile.md` so a
grader reads one file for its command.

## Commands *(shell — run first, short-circuit)*

| grader | command | rule / threshold |
|---|---|---|
| lint | `ruff check engine dashboard tests` | no lint errors |
| tests | `pytest -m "not browser"` (fixture-replay) + `pytest -m browser` (e2e) | zero failures, this session |
| type-check | `mypy engine/` | advisory — author-aid, **not** a gate step this slice |
| doctrine-lint | `doctrine_lint.py engine dashboard tests` | comment-doctrine + test-posture floor |
| special-lint | `doctrine_lint.py engine --forbid '"(critical\|warning)"@@use Severity.*'` | severities are enum constants, not string literals |
| security | `bandit -q -r engine dashboard` + `detect-secrets scan` | no high-severity SAST finding · **secrets = hard fail** |
| coverage | `pytest -m "not browser" --cov=engine --cov=dashboard --cov-report=term-missing` | changed-line ≥ 80% |
| deps | `uv export --no-dev --no-hashes \| pip-audit -r -` | **critical vuln = hard fail** · lockfile consistent · audits the **shipped tree**, not dev/security tooling |

## Other graders wired

- **logs** — run: replays a breach fixture and asserts `ALERT_RAISED{severity:critical}` fired (the
  *no-missed-critical* promise proven from the trace). Events: `ALERT_RAISED{signal,severity}`, `ALERT_CLEARED`.
- **browser / e2e** — run (**live here**, `has_ui: true`): Playwright drives the running dashboard;
  `visual_invariant` — a stale signal renders "— stale" (never a number), a CRITICAL row renders red.

## Declared n/a *(not skipped — why)*

- **schema-validation** — a reading is validated at ingest (`parse_line` rejects a malformed line), so
  there's no separate schema command.
- **codemod** — no bulk transform; this domain's drift is caught by the drift grader, not codemods.

## Allowlists + paths

- **security allowlist** — the `Severity` enum definition is `doctrine: allow` (handled by the comment
  doctrine, not here).
- **license allowlist** — MIT · BSD-2/3 · Apache-2.0 · ISC · PSF.
- **manifest paths** — `pyproject.toml` + `uv.lock`.
- **coverage exclude** — the served static HTML/JS view (the browser grader covers it, not unit coverage).
