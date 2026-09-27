---
consumed_by: [orchestrator, build]
canonical_for: `_skeleton` check rows: command, threshold, n/a reasons
profile: _skeleton
---

# Profile — `{domain}` · check-commands

The checks read this file directly for their commands, thresholds, and allowlists — the
**active-profile handshake**: the pipeline resolves `profiles/<active-profile>/check-commands.md` at run
time ([`../CONTRACT.md#active-profile-resolution`](../CONTRACT.md#active-profile-resolution)), never a
hardcoded path. Swap the profile → the checks read the new commands, unchanged. Split out of
`implement-profile.md` so each check reads *one* file for its command and profile-switching is explicit.

Row names and run order are fixed by [`../../checks/README.md`](../../checks/README.md#the-deterministic-tier-in-order).
Every row is either filled or declared n/a below; an undeclared absence is a GATE-0 finding.

## Commands *(must — one row per check, in run order)*

| check | command | rule / threshold |
|---|---|---|
| lint | {TODO} | no violations |
| type-check | {TODO, or "advisory — not a gate step"} | no errors |
| doctrine-lint | {TODO: `doctrine_lint.py` args + `--forbid` rules} | comment-doctrine + test-posture floor + domain forbids |
| codemod-check | {TODO: `codemods/<name>.py --check <path>`, or "n/a — no codemod"} | nothing left to rewrite |
| security | {TODO: SAST + secret-scan commands} | secrets = hard fail |
| tests | {TODO} | zero failures, this session |
| coverage | {TODO: coverage command} | changed-line ≥ {TODO}% |
| deps | {TODO: audit command} | critical vuln = hard fail |
| schema-validation | {TODO, or "n/a — validated at runtime"} | output matches contract |
| logs | {TODO, or "n/a"} | the required structured events fired |
| smoke | {TODO: launch · probe · stop — or "n/a — covered-by: infra" when `deploys: true`} | the process starts, answers one probe, stops |
| browser | {TODO: Playwright command + `visual_invariant`, or "n/a — `has_ui: false`"} | the visual invariant holds on the rendered DOM |
| infra | {TODO: build · up · smoke, or "n/a — `deploys: false`"} | images build · healthy on a fresh volume · migrations from empty |

## Allowlists + paths *(may — for the checks that need them)*

- **security allowlist** — {TODO or none}; vetted false positives, each with a reason (empty reason = a finding).
- **license allowlist** — {TODO}; acceptable licenses (deps check).
- **manifest paths** — {TODO}; manifest + lockfile locations (deps check's drift rule).
- **coverage exclude** — {TODO or none}; paths that don't owe coverage.

## Declared n/a *(not skipped — say why)*

{TODO: the rows above marked n/a, each with a one-line reason — e.g. "browser: API-only,
no rendered surface" · "schema: validated at ingest, no separate command". An absent check is declared
here, never silently dropped.}
