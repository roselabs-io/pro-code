---
consumed_by: ["review"]
canonical_for: "the rubric of the one independent review of a ticket's diff"
profile: agnostic
---

# Review — the one independent review of a ticket

The review reads a ticket's diff once, after every check is green. It runs in a fresh session that did
not write the diff (author ≠ reviewer), with this rubric, the active profile's `rubrics` and any
profile lens units injected into its prompt. [`skills/review-gate`](../skills/review-gate/SKILL.md) runs
it; this file is what it applies.

The review applies its lenses in the order below and reports every finding of every lens in one pass.
A finding names its lens, the file and line, what is wrong and the fix.

## 1. Feature — the acceptance criterion

- The diff satisfies the ticket's acceptance criterion on the real path, with output produced in this
  session. A claim without fresh output is a finding.
- The profile's `verify_means` say how "done" is proven in the domain; its `false_green_traps` name where
  a green result can be false (a 200 whose handler never ran). Each trap that applies to the diff is
  probed.
- A missing precondition (no test for the criterion, no rendered surface for a UI criterion) is a
  finding, not a pass.

## 2. Drift — the hooks and the conventions

- The design hooks the ticket names are applied wherever the criterion reaches (a guard on every verb,
  not only the one under test).
- The profile's conventions hold. The judgment cases of the comment doctrine and the test posture are
  read here; their regex subset is `doctrine_lint.py`'s.
- **Undeclared choices.** A library, tool, config, pattern or name that no input specified and the
  profile's declared choice-points do not cover is a finding unless `docs/assumptions.md` lists it with a
  disposition (promote to the profile / log as a decision / flag to the driver / accept).

## 3. Docs-currency — the living docs

The profile's `living_docs` set is current after the diff: shipped backlog items deleted and new ones
added (forward-only), `current-state.md` describes what is now built, a decision record exists for each
non-obvious decision, `open-questions.md` items the ticket resolved are flipped, the assumptions ledger
dispositions every undeclared choice, and a README's launch commands still work.

## 4. Simplicity — nothing beyond the ticket

Each addition in the diff traces to the ticket's acceptance criterion, a design hook the ticket names, a
profile convention, or a decision record. An addition that traces to none is a finding:

- **Speculative abstraction** — a base class, protocol, generic or plugin point with one concrete use and
  no ticket that needs a second.
- **Unrequested options** — a parameter, flag, environment variable or config key no input specified and
  no test exercises.
- **Surface the ticket did not name** — an endpoint, command, event, field or page beyond the criterion.
- **Layering beyond the hook** — the hook names a query guard; the diff adds a context object, a registry
  and a factory around it.
- **Scope creep in existing code** — renames, reformatting or refactors of lines the ticket did not touch
  (the auto-fix arm owns mechanical reformatting).
- **Defensive code for impossible states** — handling for inputs the type system or the boundary already
  excludes.

Not findings under this lens: anything a profile convention requires (a structured log event, a
migration, the per-endpoint test matrix), anything a decision record in the build justifies, tests, and
the negative case a false-green trap demands. The fix of a simplicity finding is one of two: remove the
addition, or split it to a backlog ticket with its own acceptance criterion.

The profile's `rubrics.simplicity` says what "in scope" traces to in the domain and may list items that
are always in scope.

## 5. Profile lenses

Each lens unit the active profile or overlay ships under `profiles/<x>/graders/` is applied after the
four above, with its rubric injected. A lens unit may add findings; it does not remove a finding of
another lens, and an overlay's unit cannot pass what a domain or agnostic rule fails.

## Contract

```
review(diff, rubric=<this file + the profile's rubrics + profile lens units>, context)
  → { pass, findings: [{lens, file, line, issue, fix}] }
```

- **pass** = no finding.
- Order of precedence when findings conflict: feature (correctness and completeness) > drift and
  simplicity > docs-currency. A diff that matches every convention and does not meet its criterion fails.
- The review runs once per ticket. After the author's fix pass it is not run again; the handoff lists
  each finding as fixed or open ([`skills/review-gate`](../skills/review-gate/SKILL.md)).
