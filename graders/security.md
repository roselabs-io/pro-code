# security — SAST + secret scan (deterministic · tier-1)

The **secrets-and-sinks** gate: runs the profile's static-analysis + secret-scan commands over the diff
and turns their output into findings. Deterministic, runs in the **first tier** of the code-verification
loop — before any fuzzy grader spends a token — and **short-circuits** (a leaked credential must never
reach a fuzzy lens). Agnostic: the *loop and the severities* live here; the *tools, ruleset, and allowlist*
come from the profile.

## What it checks (over the diff)

- **Secrets / credentials** — API keys, tokens, private keys, passwords, connection strings in added
  lines. **Hard fail, always** — a secret in a diff is CRITICAL and blocks the gate regardless of profile.
  The fix is remove **and** rotate (a committed secret is a leaked secret), not just delete the line.
- **Injection sinks** — untrusted input reaching SQL / shell / `eval` / deserialization / path
  construction, per the profile's SAST ruleset.
- **The profile's pack** — whatever `security_commands` the domain declares (semgrep config, bandit,
  gitleaks, a domain rule pack).

## Preconditions are findings

If the profile declares **no** security command, that's a **finding** ("no security scan configured") —
surfaced to the driver / GATE-0, never assumed clean. A scanner that errors is a finding, not a pass.

## Profile hooks (`profiles/<active-profile>/check-commands.md`)

- **security commands** — the SAST + secret-scan commands to run (+ how to parse their output).
- **security allowlist** *(may)* — vetted false positives, each with a reason (an empty reason is itself a finding).
- **severity map** *(may)* — domain overrides, but **secrets stay CRITICAL**: a profile may *raise* a
  severity, never *lower* the secret floor (the additive-only rule, applied to severity).

## Contract

```
grade(diff, rubric=<security_commands + allow>, context)
  → { pass, findings: [{file, line, rule, severity, fix}], hard_fail_on: secret }
```

Deterministic — facts, not judgment; runs first, short-circuits. Logic-level flaws a scanner can't catch
(authz ordering, an existence oracle) stay with the **drift / core-promise** graders — this grader is the
mechanical floor. See [`code-verification-loop.md`](code-verification-loop.md) ·
[`../profiles/CONTRACT.md`](../profiles/CONTRACT.md).

> **Provenance:** built independently in pro-code and DTS, then cross-checked — the core design converged.
> The remove-**and**-rotate rule + the "raise, never lower the secret floor" severity rule originated here
> and were adopted in both. Agnostic — no domain content (the machine-safety / hardware traps live in the
> DTS profile).
