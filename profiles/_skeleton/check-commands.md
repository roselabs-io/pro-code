# Profile — `{domain}` · check-commands

The deterministic graders read this file directly for their commands, thresholds, and allowlists — the
**active-profile handshake**: the pipeline resolves `profiles/<active-profile>/check-commands.md` at run
time, never a hardcoded path. Swap the profile → the graders read the new commands, unchanged. Split out
of `implement-profile.md` so each grader reads *one* file for its command and profile-switching is explicit.

## Commands *(must — one row per deterministic grader this domain runs)*

| grader | command | rule / threshold |
|---|---|---|
| lint | {TODO} | no violations |
| tests | {TODO} | zero failures, this session |
| type-check | {TODO, or "advisory — not a gate step"} | no errors |
| doctrine-lint | {TODO: `doctrine_lint.py` args + `--forbid` rules} | comment-doctrine + test-posture floor + domain forbids |
| security | {TODO: SAST + secret-scan commands} | secrets = hard fail |
| coverage | {TODO: coverage command} | changed-line ≥ {TODO}% |
| deps | {TODO: audit command} | critical vuln = hard fail |
| schema-validation | {TODO, or "n/a — validated at runtime"} | output matches contract |
| logs | {TODO, or "n/a"} | the required structured events fired |

## Allowlists + paths *(may — for the graders that need them)*

- **security allowlist** — {TODO or none}; vetted false positives, each with a reason (empty reason = a finding).
- **license allowlist** — {TODO}; acceptable licenses (deps grader).
- **manifest paths** — {TODO}; manifest + lockfile locations (deps grader's drift check).
- **coverage exclude** — {TODO or none}; paths that don't owe coverage.

## Declared n/a *(not skipped — say why)*

{TODO: agnostic graders this domain does NOT run, each with a one-line reason — e.g. "browser: API-only,
no rendered surface" · "schema: validated at ingest, no separate command". An absent grader is declared
here, never silently dropped.}
