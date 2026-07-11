# coverage — changed-line test coverage (deterministic · tier-1)

Grades whether the **diff's** new/changed lines are exercised by tests — a *delta* check, not a whole-repo
percentage. Deterministic, tier-1, short-circuits. Agnostic: the *rule* (changed lines must be covered; a
drop is a finding; no test at all is the loudest finding) lives here; the *command, floor, and exclusions*
come from the profile.

## What it checks (over the diff)

- **Changed-line coverage** — every new/changed *coverable* line in the diff is hit by at least one test in
  this run. Uncovered changed lines → findings (file:line).
- **No regression** — total coverage did not drop versus the base.
- **The floor** — changed-line coverage meets the profile's threshold (e.g. ≥ 80%).

## Preconditions are findings

A change with **no test at all** is the loudest finding — *"untested change"* — never a silent pass (the
precondition-is-a-finding rule). The fix pass can *write* the missing test; this grader's job is to refuse
to call it done without one. Non-coverable lines (pure declarations, generated code) are excluded per the
profile — declared, not hand-waved.

## Profile hooks (`profiles/<active-profile>/check-commands.md`)

- **coverage command** — how coverage is measured (`pytest --cov`, `vitest --coverage`, …).
- **coverage floor** — the changed-line threshold.
- **coverage exclude** *(may)* — paths/patterns that don't owe coverage (declared, not skipped).

## Contract

```
grade(diff, rubric=<coverage_command + floor>, context)
  → { pass, findings: [{file, line, issue: uncovered | regression | no-test, fix}] }
```

Deterministic. **Coverage proves a line *ran* under test — not that the test *asserts* the right thing.**
That's the feature grader + the test-posture floor. Pair them: coverage = reach, posture = quality; a
line can be 100% covered by an assert-less smoke test and still be untested in the way that matters. See
[`code-verification-loop.md`](code-verification-loop.md) ·
[`../doc-patterns/doctrines/test-posture.md`](../doc-patterns/doctrines/test-posture.md).

> **Provenance:** built independently in pro-code and DTS, then cross-checked — the core design converged
> (deterministic · tier-1 · short-circuit · precondition-is-a-finding · scoped-to-diff). The
> coverage≠assertion pairing originated here and was adopted in both. Agnostic — the *behaviour-on-hardware*
> pairing is a DTS-profile addition.
