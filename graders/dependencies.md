# dependencies — supply-chain gate (deterministic · tier-1)

Grades **new or changed dependencies** in the diff: vetted, vuln-free, lockfile-consistent, license-clean.
Deterministic, tier-1, short-circuits — a known-vulnerable dep must never reach a fuzzy lens. Agnostic: the
*checks* live here; the *audit command, license allowlist, and manifest paths* come from the profile.

## What it checks (over the diff)

- **Known vulnerabilities** — every added/bumped dep passes the profile's audit (`pip-audit` / `npm audit`
  / `osv-scanner`). A known CRITICAL vuln is a **hard fail**.
- **Lockfile consistency** — a manifest change carries a matching, coherent lockfile update: no drift, no
  phantom or unpinned adds, no lockfile bump without a manifest reason.
- **License** — each new dep's license is on the profile's allowlist; an unknown or forbidden license is a
  finding.
- **Provenance smell** *(may)* — typosquat / abandoned / just-published heuristics, if the profile enables them.

## Preconditions are findings

A dep added **without** touching the lockfile → finding (drift). No audit command declared → finding
("no supply-chain scan configured"), not a silent pass.

## Profile hooks (`profiles/<active-profile>/check-commands.md`)

- **deps audit command** — the vuln/audit command (+ how to parse).
- **license allowlist** — acceptable licenses.
- **manifest paths** — manifest + lockfile locations for the drift check.

## Contract

```
grade(diff, rubric=<audit + license + manifest>, context)
  → { pass, findings: [{dep, issue: vuln | lockfile-drift | license | provenance, severity, fix}],
      hard_fail_on: critical-vuln }
```

Deterministic — facts. **Scoped to deps the diff introduces or bumps**, not a full-tree audit every gate
(that's a periodic job, not a per-change gate — the whole tree doesn't change every ticket). See
[`code-verification-loop.md`](code-verification-loop.md) · [`../profiles/CONTRACT.md`](../profiles/CONTRACT.md).

> **Provenance:** built independently in pro-code and DTS, then cross-checked — the core design converged.
> The hard-fail-on-critical + scoped-to-diff-not-full-tree framing originated here and were adopted in both.
> Agnostic — no domain delta.
