---
consumed_by: [check:runtime-smoke]
canonical_for: the runtime-smoke check
profile: agnostic
---

# Check — runtime-smoke (boots-at-all floor · non-deploying profiles)

Starts the app the way its README says to, sends it one request or one invocation, asserts a
response, stops it. The floor under every other runtime check: **tests green ≠ the process starts.**
An import cycle, a missing env var read at module load, a port already bound, a `main()` that no
entry point calls — every unit test passes and nothing runs.

Applies to profiles with `deploys: false`. A deploying profile runs [`infra.md`](infra.md) instead,
which subsumes this (compose up + smoke is the same assertion against the shipped image). A UI-bearing
profile runs [`browser.md`](browser.md) on top of either; browser boots the app too, but asserts the
DOM, not the boot — the smoke row stays declared and may say `covered-by: browser`.

## What it checks

- **It starts** — the profile's launch command brings the process up within a bounded wait.
- **It answers** — one request (or one CLI invocation, or one import + call for a library) returns the
  expected status or output. For an HTTP app the default probe is the framework's self-describing
  endpoint (`GET /openapi.json` → 200 for FastAPI), so the probe is profile-generic, not example-specific.
- **It stops** — the process is torn down; a leaked process is a finding.

## Preconditions are findings

No launch command declared → finding ("no runtime smoke configured"). A README "Run it" section that
names a command the profile's smoke row does not use → finding (the README doctrine and this check
must agree on how the thing starts).

## Profile hooks (`profiles/<active-profile>/check-commands.md`)

- **smoke row** — `launch` (how to start), `probe` (the request/invocation + expected result), `stop`.
  Or `n/a — covered-by: infra` when `deploys: true`; or `covered-by: browser` when the browser row's
  fixture boots the same process.

## Contract

```
check(diff, config=<launch + probe + stop>, context)
  → { pass, findings: [{issue: no-start | no-answer | leaked-process | no-smoke-configured, detail}] }
```

Deterministic; runs in the verify beat after tests, before browser/infra
([the order](README.md#the-deterministic-tier-in-order)). Proves the process boots and answers — not
that the answer is right; that is the tests' and the feature grader's job.

> **Provenance:** ported from the DTS harness (2026-09), where it exists as the boots-at-all floor for
> profiles that neither deploy nor render. In pro-code the gap was `generic-saas`: API-only, no
> `has_ui`, no `deploys`, so nothing in the loop ever started the process.
